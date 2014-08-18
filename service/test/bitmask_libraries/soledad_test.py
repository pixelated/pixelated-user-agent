from mock import patch
from app.bitmask_libraries.soledad import SoledadSession
from abstract_leap_test import AbstractLeapTest


@patch('app.bitmask_libraries.soledad.Soledad')
class SoledadSessionTest(AbstractLeapTest):

    def setUp(self):
        # given
        self.provider.fetch_soledad_json.return_value = {'hosts': {
            'couch1': {
                'hostname': 'couch1.some-server.test',
                'ip_address': '192.168.1.1',
                'port': 1234
            }
        }}

    @patch('app.bitmask_libraries.soledad.Soledad.__init__')
    def test_that_soledad_is_created_with_required_params(self, soledad_mock, init_mock):
        # when
        SoledadSession(self.provider, 'any-passphrase', self.srp_session)

        # then
        init_mock.assert_called_with(self.uuid, 'any-passphrase', '%s/soledad/%s.secret' % (self.leap_home, self.uuid),
                                     '%s/soledad/%s.db' % (self.leap_home, self.uuid),
                                     'https://couch1.some-server.test:1234/user-%s' % self.uuid,
                                     '/some/path/to/ca_cert', self.token)

    def test_that_sync_is_called(self, soledad_mock):
            instance = soledad_mock.return_value
            instance.server_url = '/foo/bar'
            instance.need_sync.return_value = True
            soledad_session = SoledadSession(self.provider, 'any-passphrase', self.srp_session)

            # when
            soledad_session.sync()

            # then
            instance.need_sync.assert_called_with('/foo/bar')
            instance.sync.assert_called_with()

    def test_that_sync_not_called_if_not_needed(self, mock):
            instance = mock.return_value
            instance.server_url = '/foo/bar'
            instance.need_sync.return_value = False
            soledad_session = SoledadSession(self.provider, 'any-passphrase', self.srp_session)

            # when
            soledad_session.sync()

            # then
            instance.need_sync.assert_called_with('/foo/bar')
            self.assertFalse(instance.sync.called)
