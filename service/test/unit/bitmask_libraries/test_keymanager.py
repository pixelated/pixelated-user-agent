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
from mockito import when

from test_abstract_leap import AbstractLeapTest
from leap.keymanager import openpgp, KeyNotFound
from pixelated.bitmask_libraries.keymanager import Keymanager
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.config import leap_config


class KeymanagerTest(AbstractLeapTest):
    @patch('pixelated.bitmask_libraries.keymanager.KeyManager')
    def test_that_keymanager_is_created(self, keymanager_mock):
        when(self.provider)._discover_nicknym_server().thenReturn('https://nicknym.some-server.test:6425/')
        self.provider.combined_cerfificates_path = 'combined_cerfificates_path'
        self.provider.provider_api_cert = '/some/path/to/provider_ca_cert'
        leap_config.gpg_binary = '/path/to/gpg'

        Keymanager(self.provider,
                   self.soledad,
                   'test_user@some-server.test',
                   self.auth.token,
                   self.auth.uuid)

        keymanager_mock.assert_called_with(
            'test_user@some-server.test',
            'https://nicknym.some-server.test:6425/',
            self.soledad,
            token=self.auth.token,
            ca_cert_path='/some/path/to/provider_ca_cert',
            api_uri='https://api.some-server.test:4430',
            api_version='1',
            uid=self.auth.uuid,
            gpgbinary='/path/to/gpg',
            combined_ca_bundle='combined_cerfificates_path')

    @patch('pixelated.bitmask_libraries.keymanager.KeyManager')
    def test_gen_key(self, keymanager_mock):
        # given
        keyman = keymanager_mock.return_value
        keyman.get_key.side_effect = KeyNotFound
        keymanager = Keymanager(self.provider,
                                self.soledad,
                                'test_user@some-server.test',
                                self.auth.token,
                                self.auth.uuid)

        # when/then
        keymanager.generate_openpgp_key()

        keyman.get_key.assert_called_with('test_user@some-server.test', private=True, fetch_remote=False)
        keyman.gen_key.assert_called()
