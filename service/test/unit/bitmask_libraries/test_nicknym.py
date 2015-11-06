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
from mock import patch

from test_abstract_leap import AbstractLeapTest
from leap.keymanager import openpgp, KeyNotFound
from pixelated.bitmask_libraries.nicknym import NickNym
from pixelated.bitmask_libraries.certs import LeapCertificate


class NickNymTest(AbstractLeapTest):
    @patch('pixelated.bitmask_libraries.nicknym.KeyManager.__init__', return_value=None)
    def test_that_keymanager_is_created(self, keymanager_init_mock):
        # given
        LeapCertificate.provider_api_cert = '/some/path/to/provider_ca_cert'
        # when
        NickNym(self.provider,
                self.config,
                self.soledad,
                'test_user@some-server.test',
                self.auth.token,
                self.auth.uuid)

        # then
        keymanager_init_mock.assert_called_with(
            'test_user@some-server.test',
            'https://nicknym.some-server.test:6425/',
            self.soledad,
            token=self.auth.token,
            ca_cert_path='/some/path/to/provider_ca_cert',
            api_uri='https://api.some-server.test:4430',
            api_version='1',
            uid=self.auth.uuid,
            gpgbinary='/path/to/gpg')

    @patch('pixelated.bitmask_libraries.nicknym.KeyManager')
    def test_gen_key(self, keymanager_mock):
        # given
        keyman = keymanager_mock.return_value
        keyman.get_key.side_effect = KeyNotFound
        nicknym = NickNym(self.provider,
                          self.config,
                          self.soledad,
                          'test_user@some-server.test',
                          self.auth.token,
                          self.auth.uuid)

        # when/then
        nicknym.generate_openpgp_key()

        keyman.get_key.assert_called_with('test_user@some-server.test', openpgp.OpenPGPKey, private=True, fetch_remote=False)
        keyman.gen_key.assert_called_with(openpgp.OpenPGPKey)
