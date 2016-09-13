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
from leap.keymanager import KeyManager, KeyNotFound
from pixelated.config import leap_config
from twisted.internet import defer
import logging

logger = logging.getLogger(__name__)


class UploadKeyError(Exception):
    pass


class Keymanager(object):
    def __init__(self, provider, soledad, email_address, token, uuid):
        nicknym_url = provider._discover_nicknym_server()
        self._email = email_address
        self.keymanager = KeyManager(self._email, nicknym_url,
                                     soledad,
                                     token=token, ca_cert_path=provider.provider_api_cert, api_uri=provider.api_uri,
                                     api_version=provider.api_version,
                                     uid=uuid, gpgbinary=leap_config.gpg_binary,
                                     combined_ca_bundle=provider.combined_cerfificates_path)

    @defer.inlineCallbacks
    def generate_openpgp_key(self):
        key_present = yield self._key_exists(self._email)
        if not key_present:
            logger.info("Generating keys - this could take a while...")
            yield self._gen_key()
            try:
                yield self._send_key_to_leap()
            except Exception as e:
                yield self.delete_key_pair(self._email)
                raise UploadKeyError(e.message)

    @defer.inlineCallbacks
    def _key_exists(self, email):
        try:
            yield self.get_key(email, private=True, fetch_remote=False)
            defer.returnValue(True)
        except KeyNotFound:
            defer.returnValue(False)

    def get_key(self, email, private=False, fetch_remote=True):
        return self.keymanager.get_key(email, private=private, fetch_remote=fetch_remote)

    def _gen_key(self):
        return self.keymanager.gen_key()

    def _send_key_to_leap(self):
        return self.keymanager.send_key()

    @defer.inlineCallbacks
    def delete_key_pair(self, key):
        private_key = yield self.get_key(self._email, private=True, fetch_remote=False)
        public_key = yield self.get_key(self._email, private=False, fetch_remote=False)

        self.keymanager.delete_key(private_key)
        self.keymanager.delete_key(public_key)
