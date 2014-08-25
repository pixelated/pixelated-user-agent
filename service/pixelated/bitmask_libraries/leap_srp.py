#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
import binascii
import json
import requests

from requests import Session
from srp import User, srp, create_salted_verification_key
from requests.exceptions import HTTPError, SSLError, Timeout
from config import SYSTEM_CA_BUNDLE

REGISTER_USER_LOGIN_KEY = 'user[login]'
REGISTER_USER_VERIFIER_KEY = 'user[password_verifier]'
REGISTER_USER_SALT_KEY = 'user[password_salt]'


class LeapAuthException(Exception):
    def __init__(self, *args, **kwargs):
        super(LeapAuthException, self).__init__(*args, **kwargs)


class LeapSRPSession(object):
    def __init__(self, user_name, api_server_name, uuid, token, session_id, api_version='1'):
        self.user_name = user_name
        self.api_server_name = api_server_name
        self.uuid = uuid
        self.token = token
        self.session_id = session_id
        self.api_version = api_version

    def __str__(self):
        return 'LeapSRPSession(%s, %s, %s, %s, %s, %s)' % (self.user_name, self.api_server_name, self.uuid, self.token, self.session_id, self.api_version)


class LeapSecureRemotePassword(object):
    def __init__(self, hash_alg=srp.SHA256, ng_type=srp.NG_1024, ca_bundle=SYSTEM_CA_BUNDLE, timeout_in_s=15,
                 leap_api_version='1'):

        self.hash_alg = hash_alg
        self.ng_type = ng_type
        self.timeout_in_s = timeout_in_s
        self.ca_bundle = ca_bundle
        self.leap_api_version = leap_api_version

    def authenticate(self, api_uri, username, password):
        session = Session()
        try:
            return self._authenticate_with_session(session, api_uri, username, password)
        except Timeout, e:
            raise LeapAuthException(e)
        finally:
            session.close()

    def _authenticate_with_session(self, http_session, api_uri, username, password):
        try:
            srp_user = User(username.encode('utf-8'), password.encode('utf-8'), self.hash_alg, self.ng_type)

            salt, B_challenge = self._begin_authentication(srp_user, http_session, api_uri)
            M2_verfication_code, leap_session = self._process_challenge(srp_user, http_session, api_uri, salt,
                                                                        B_challenge)
            self._verify_session(srp_user, M2_verfication_code)

            return leap_session
        except (HTTPError, SSLError), e:
            raise LeapAuthException(e)

    def _begin_authentication(self, user, session, api_uri):
        _, A = user.start_authentication()

        auth_data = {
            "login": user.get_username(),
            "A": binascii.hexlify(A)
        }
        session_url = '%s/%s/sessions' % (api_uri, self.leap_api_version)
        response = session.post(session_url, data=auth_data, verify=self.ca_bundle, timeout=self.timeout_in_s)
        response.raise_for_status()
        json_content = json.loads(response.content)

        salt = _safe_unhexlify(json_content.get('salt'))
        B = _safe_unhexlify(json_content.get('B'))

        return salt, B

    def _process_challenge(self, user, session, api_uri, salt, B):
        M = user.process_challenge(salt, B)

        auth_data = {
            "client_auth": binascii.hexlify(M)
        }

        auth_url = '%s/%s/sessions/%s' % (api_uri, self.leap_api_version, user.get_username())
        response = session.put(auth_url, data=auth_data, verify=self.ca_bundle, timeout=self.timeout_in_s)
        response.raise_for_status()
        auth_json = json.loads(response.content)

        M2 = _safe_unhexlify(auth_json.get('M2'))
        uuid = auth_json.get('id')
        token = auth_json.get('token')
        session_id = response.cookies.get('_session_id')

        return M2, LeapSRPSession(user.get_username(), api_uri, uuid, token, session_id)

    def _verify_session(self, user, M2):
        user.verify_session(M2)
        if not user.authenticated():
            raise LeapAuthException()

    def register(self, api_uri, username, password):
        try:
            salt, verifier = create_salted_verification_key(username, password, self.hash_alg, self.ng_type)
            return self._post_registration_data(api_uri, username, salt, verifier)
        except (HTTPError, SSLError, Timeout), e:
            raise LeapAuthException(e)

    def _post_registration_data(self, api_uri, username, salt, verifier):
        users_url = '%s/%s/users' % (api_uri, self.leap_api_version)

        user_data = {
            REGISTER_USER_LOGIN_KEY: username,
            REGISTER_USER_SALT_KEY: binascii.hexlify(salt),
            REGISTER_USER_VERIFIER_KEY: binascii.hexlify(verifier)
        }

        response = requests.post(users_url, data=user_data, verify=self.ca_bundle, timeout=self.timeout_in_s)
        response.raise_for_status()
        reg_json = json.loads(response.content)

        return reg_json['ok']


def _safe_unhexlify(hex_str):
    return binascii.unhexlify(hex_str) \
        if (len(hex_str) % 2 == 0) else binascii.unhexlify('0' + hex_str)
