from mock import patch

from leap.keymanager import openpgp, KeyNotFound
from pixelated.bitmask_libraries.nicknym import NickNym
from abstract_leap_test import AbstractLeapTest


class NickNymTest(AbstractLeapTest):
    @patch('pixelated.bitmask_libraries.nicknym.KeyManager.__init__', return_value=None)
    def test_that_keymanager_is_created(self, init_mock):
        # given

        # when
        NickNym(self.provider, self.config, self.soledad_session, self.srp_session)

        # then
        init_mock.assert_called_with('test_user@some-server.test', 'https://nicknym.some-server.test:6425/',
                                     self.soledad, self.token, '/some/path/to/ca_cert',
                                     'https://api.some-server.test:4430', '1', self.uuid,
                                     '/path/to/gpg')

    @patch('pixelated.bitmask_libraries.nicknym.KeyManager')
    def test_gen_key(self, keymanager_mock):
        # given
        keyman = keymanager_mock.return_value
        keyman.get_key.side_effect = KeyNotFound
        nicknym = NickNym(self.provider, self.config, self.soledad_session, self.srp_session)

        # when/then
        nicknym.generate_openpgp_key()

        keyman.get_key.assert_called_with('test_user@some-server.test', openpgp.OpenPGPKey, fetch_remote=False, private=True)
        keyman.gen_key.assert_called_with(openpgp.OpenPGPKey)
