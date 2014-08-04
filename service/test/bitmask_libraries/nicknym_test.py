from mock import patch

from app.bitmask_libraries.nicknym import NickNym
from abstract_leap_test import AbstractLeapTest


class NickNymTest(AbstractLeapTest):
    @patch('app.bitmask_libraries.nicknym.KeyManager.__init__', return_value=None)
    def test_that_keymanager_is_created(self, init_mock):
        #given

        #when
        NickNym(self.provider, self.config, self.soledad_session, self.srp_session)

        #then
        init_mock.assert_called_with('test_user@some-server.test', 'https://nicknym.some-server.test:6425/',
                                     self.soledad, self.session_id, '/some/path/to/ca_cert',
                                     'https://api.some-server.test:4430', '1', self.uuid,
                                     '/path/to/gpg')
