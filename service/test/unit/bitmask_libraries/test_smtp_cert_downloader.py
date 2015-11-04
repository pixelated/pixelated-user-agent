#
# Copyright (c) 2015 ThoughtWorks, Inc.
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
import unittest
from mockito import mock, unstub
from requests import HTTPError
from pixelated.bitmask_libraries.session import SmtpCertDownloader
from tempfile import NamedTemporaryFile
from httmock import all_requests, HTTMock, urlmatch

CERTIFICATE_DATA = 'some cert data'


@all_requests
def not_found_mock(url, request):
    return {'status_code': 404,
            'content': 'foobar'}


@urlmatch(netloc='api.some-server.test:4430', path='/1/cert')
def ca_cert_mock(url, request):
    return {
        "status_code": 200,
        "content": CERTIFICATE_DATA
    }


class TestSmtpCertDownloader(unittest.TestCase):

    def setUp(self):
        self._provider = mock()
        self._config = mock()
        self._config.leap_home = '/tmp'
        self._auth = mock()

        self._provider.config = self._config
        self._provider.api_uri = 'https://api.some-server.test:4430'
        self._provider.api_version = '1'
        self._provider.server_name = 'some.host.tld'

        self._auth.session_id = 'some session id'
        self._auth.token = 'some token'

    def tearDown(self):
        unstub()

    def test_download_certificate(self):
        with HTTMock(ca_cert_mock, not_found_mock):
            cert_data = SmtpCertDownloader(self._provider, self._auth).download()

        self.assertEqual(CERTIFICATE_DATA, cert_data)

    def test_error_if_not_found(self):
        downloader = SmtpCertDownloader(self._provider, self._auth)
        with HTTMock(not_found_mock):
            self.assertRaises(HTTPError, downloader.download)

    def test_download_to(self):
        downloader = SmtpCertDownloader(self._provider, self._auth)

        with NamedTemporaryFile() as tmp_file:
            with HTTMock(ca_cert_mock, not_found_mock):
                downloader.download_to(tmp_file.name)

            file_content = open(tmp_file.name).read()
            self.assertEqual(CERTIFICATE_DATA, file_content)
