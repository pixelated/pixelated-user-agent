import os
from mock import MagicMock, patch
from abstract_leap_test import AbstractLeapTest
from pixelated.bitmask_libraries.smtp import LeapSmtp
from httmock import all_requests, HTTMock, urlmatch


@all_requests
def not_found_mock(url, request):
    sys.stderr.write('url=%s\n' % url.netloc)
    sys.stderr.write('path=%s\n' % url.path)
    return {'status_code': 404,
            'content': 'foobar'}


@urlmatch(netloc='api.some-server.test:4430', path='/1/cert')
def ca_cert_mock(url, request):
    return {
        "status_code": 200,
        "content": "some content"
    }


class LeapSmtpTest(AbstractLeapTest):
    keymanager = MagicMock()

    def setUp(self):
        self.provider.fetch_smtp_json.return_value = {
            'hosts': {
                'leap-mx': {
                    'hostname': 'smtp.some-sever.test',
                    'port': '1234'
                }
            }
        }
        self.config.timeout_in_s = 15

    def test_that_client_cert_gets_downloaded(self):
        smtp = LeapSmtp(self.provider, self.keymanager, self.srp_session)

        with HTTMock(ca_cert_mock, not_found_mock):
            smtp._download_client_certificates()

            path = self._client_cert_path()
            self.assertTrue(os.path.isfile(path))

    def _client_cert_path(self):
        return os.path.join(self.leap_home, 'providers', 'some-server.test', 'keys', 'client', 'smtp.pem')

    @patch('pixelated.bitmask_libraries.smtp.setup_smtp_gateway')
    def test_that_start_calls_setup_smtp_gateway(self, gateway_mock):
        smtp = LeapSmtp(self.provider, self.keymanager, self.srp_session)
        port = 500
        smtp._twisted_port = port
        gateway_mock.return_value = (None, None)
        with HTTMock(ca_cert_mock, not_found_mock):
            smtp.start()

        cert_path = self._client_cert_path()
        gateway_mock.assert_called_with(keymanager=self.keymanager, smtp_cert=cert_path, smtp_key=cert_path, userid='test_user@some-server.test', smtp_port='1234', encrypted_only=False, smtp_host='smtp.some-sever.test', port=port)

    def test_that_client_stop_does_nothing_if_not_started(self):
        smtp = LeapSmtp(self.provider, self.keymanager, self.srp_session)

        with HTTMock(not_found_mock):
            smtp.stop()

    @patch('pixelated.bitmask_libraries.smtp.setup_smtp_gateway')
    def test_that_running_smtp_sevice_is_stopped(self, gateway_mock):
        smtp = LeapSmtp(self.provider, self.keymanager, self.srp_session)

        smtp_service = MagicMock()
        smtp_port = MagicMock()
        gateway_mock.return_value = (smtp_service, smtp_port)

        with HTTMock(ca_cert_mock, not_found_mock):
            smtp.start()
            smtp.stop()

        smtp_port.stopListening.assert_called_with()
        smtp_service.doStop.assert_called_with()
