#
# Copyright (c) 2016 ThoughtWorks, Inc.
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
import os
import unittest
import tempdir
from pixelated.bitmask_libraries import session
from leap.srp_session import SRPSession
import leap.common.certs as certs
from mockito import mock, unstub, when, verify, never, any as ANY

from pixelated.bitmask_libraries.session import SmtpClientCertificate


class TestSmtpClientCertificate(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempdir.TempDir()
        self.provider = mock()
        self.provider.domain = 'some-provider.tld'
        self.auth = SRPSession('username', 'token', 'uuid', 'session_id')
        self.pem_path = os.path.join(self.tmp_dir.name, 'providers', 'some-provider.tld', 'keys', 'client', 'smtp.pem')
        self.downloader = mock()
        when(session).SmtpCertDownloader(self.provider, self.auth).thenReturn(self.downloader)

    def tearDown(self):
        self.tmp_dir.dissolve()
        unstub()

    def test_download_certificate(self):
        cert = SmtpClientCertificate(self.provider, self.auth, self.tmp_dir.name)
        result = cert.cert_path()

        self.assertEqual(self.pem_path, result)
        verify(self.downloader).download_to(self.pem_path)

    def test_download_certificate_if_redownload_necessary_e_g_certificate_expired(self):
        self.pretend_all_paths_exist()
        when(certs).should_redownload(self.pem_path).thenReturn(True)

        cert = SmtpClientCertificate(self.provider, self.auth, self.tmp_dir.name)
        result = cert.cert_path()

        self.assertEqual(self.pem_path, result)
        verify(self.downloader).download_to(self.pem_path)

    def pretend_all_paths_exist(self):
        when(os.path).exists(ANY()).thenReturn(True)

    def test_skip_download_if_already_downloaded_and_still_valid(self):
        when(os.path).exists(self.pem_path).thenReturn(True)
        when(certs).should_redownload(ANY()).thenReturn(False)
        cert = SmtpClientCertificate(self.provider, self.auth, self.tmp_dir.name)
        result = cert.cert_path()

        self.assertEqual(self.pem_path, result)
        verify(self.downloader, never).download_to(ANY())
