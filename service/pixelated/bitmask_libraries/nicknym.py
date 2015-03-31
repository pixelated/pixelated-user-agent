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
from leap.keymanager import KeyManager, openpgp, KeyNotFound
from .certs import which_api_CA_bundle


class NickNym(object):
    def __init__(self, provider, config, soledad_session, srp_session):
        nicknym_url = _discover_nicknym_server(provider)
        self._email = '%s@%s' % (srp_session.user_name, provider.domain)
        self.keymanager = KeyManager('%s@%s' % (srp_session.user_name, provider.domain), nicknym_url,
                                     soledad_session.soledad,
                                     srp_session.token, which_api_CA_bundle(provider), provider.api_uri,
                                     provider.api_version,
                                     srp_session.uuid, config.gpg_binary)

    def generate_openpgp_key(self):
        if not self._key_exists(self._email):
            print "Generating keys - this could take a while..."
            self._gen_key()
            self._send_key_to_leap()

    def _key_exists(self, email):
        try:
            self.keymanager.get_key(email, openpgp.OpenPGPKey, private=True, fetch_remote=False)
            return True
        except KeyNotFound:
            return False

    def _gen_key(self):
        self.keymanager.gen_key(openpgp.OpenPGPKey)

    def _send_key_to_leap(self):
        self.keymanager.send_key(openpgp.OpenPGPKey)


def _discover_nicknym_server(provider):
    return 'https://nicknym.%s:6425/' % provider.domain
