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
import sys

import os
from mock import MagicMock, patch
from test_abstract_leap import AbstractLeapTest
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
        super(LeapSmtpTest, self).setUp()
        self.provider.fetch_smtp_json.return_value = {
            'hosts': {
                'leap-mx': {
                    'hostname': 'smtp.some-sever.test',
                    'port': '1234'
                }
            }
        }
        self.config.timeout_in_s = 15

    def _client_cert_path(self):
        return os.path.join(self.leap_home, 'providers', 'some-server.test', 'keys', 'client', 'smtp.pem')

    @patch('pixelated.bitmask_libraries.smtp.setup_smtp_gateway')
    def test_that_start_calls_setup_smtp_gateway(self, gateway_mock):
        self.provider.smtp_info = MagicMock(return_value=('smtp.some-sever.test', 1234))
        self.provider._client_cert_path = MagicMock(return_value=self._client_cert_path())
        smtp = LeapSmtp(self.provider, self.auth, self.keymanager)

        port = 500
        smtp.local_smtp_port_number = port
        gateway_mock.return_value = (None, None)
        with HTTMock(ca_cert_mock, not_found_mock):
            smtp.ensure_running()

        cert_path = self._client_cert_path()
        gateway_mock.assert_called_with(smtp_cert=cert_path, userid='test_user@some-server.test', smtp_port=1234, smtp_key=cert_path, keymanager=self.keymanager, encrypted_only=False, smtp_host='smtp.some-sever.test', port=port)

    def test_that_client_stop_does_nothing_if_not_started(self):
        self.provider.smtp_info = MagicMock(return_value=('smtp.some-sever.test', 1234))
        smtp = LeapSmtp(self.provider, self.auth, self.keymanager)

        with HTTMock(not_found_mock):
            smtp.stop()

    @patch('pixelated.bitmask_libraries.smtp.setup_smtp_gateway')
    def test_that_running_smtp_sevice_is_stopped(self, gateway_mock):
        self.provider.smtp_info = MagicMock(return_value=('smtp.some-sever.test', 1234))
        smtp = LeapSmtp(self.provider, self.auth, self.keymanager)

        smtp_service = MagicMock()
        smtp_port = MagicMock()
        gateway_mock.return_value = (smtp_service, smtp_port)

        with HTTMock(ca_cert_mock, not_found_mock):
            smtp.ensure_running()
            smtp.stop()

        smtp_port.stopListening.assert_called_with()
        smtp_service.doStop.assert_called_with()
