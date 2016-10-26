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
import getpass
import re
import sys
from collections import namedtuple

from leap.bitmask.bonafide.provider import Api
from leap.bitmask.bonafide.session import Session
from leap.common.events import server as events_server
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.config import arguments
from pixelated.config import logger as logger_config
from pixelated.config.authentication import Authentication
from pixelated.config.sessions import LeapSessionFactory
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

Credentials = namedtuple('Credentials', 'username, password')

logger = Logger()


def _validate(username, password):
    try:
        validate_username(username)
        validate_password(password)
    except ValueError, e:
        print(e.message)
        sys.exit(1)


def _set_provider(provider_cert, provider_cert_fingerprint, server_name):
    events_server.ensure_server()
    LeapCertificate.set_cert_and_fingerprint(provider_cert, provider_cert_fingerprint)
    provider = LeapProvider(server_name)
    provider.setup_ca()
    provider.download_settings()
    return provider


def _bonafide_session(username, password, provider):
    srp_provider = Api(provider.api_uri)
    credentials = Credentials(username, password)
    return Session(credentials, srp_provider, provider.local_ca_crt)


@inlineCallbacks
def _bootstrap_leap_session(username, password, leap_provider, srp_auth):
    auth = Authentication(username, srp_auth.token, srp_auth.uuid, 'session_id', {'is_admin': False})
    yield LeapSessionFactory(leap_provider).create(username, password, auth)


@inlineCallbacks
def register(server_name, username, password, leap_home, provider_cert, provider_cert_fingerprint):
    if not password:
        password = getpass.getpass('Please enter password for %s: ' % username)

    _validate(username, password)
    leap_provider = _set_provider(provider_cert, provider_cert_fingerprint, server_name)
    srp_auth = _bonafide_session(username, password, leap_provider)

    created, user = yield srp_auth.signup(username, password, invite=None)
    if created:
        yield _bootstrap_leap_session(username, password, leap_provider, srp_auth)
    else:
        logger.error("Register failed")


def validate_username(username):
    accepted_characters = '^[a-z0-9\-\_\.]*$'
    if (not re.match(accepted_characters, username)):
        raise ValueError('Only lowercase letters, digits, . - and _ allowed.')


def validate_password(password):
    if len(password) < 8:
        raise ValueError('The password must have at least 8 characters')


def initialize():
    logger_config.init(debug=False)
    args = arguments.parse_register_args()
    register(
        args.provider,
        args.username,
        args.password,
        args.leap_home,
        args.leap_provider_cert,
        args.leap_provider_cert_fingerprint)
