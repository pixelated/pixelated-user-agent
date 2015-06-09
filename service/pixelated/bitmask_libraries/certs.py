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
import os


class LeapCertificate(object):

    LEAP_CERT = None
    LEAP_FINGERPRINT = None

    def __init__(self, provider):
        self._config = provider.config
        self._server_name = provider.server_name
        self._provider = provider

    @staticmethod
    def set_cert_and_fingerprint(cert_file=None, cert_fingerprint=None):
        if cert_fingerprint is None:
            LeapCertificate.LEAP_CERT = cert_file or True
            LeapCertificate.LEAP_FINGERPRINT = None
        else:
            LeapCertificate.LEAP_FINGERPRINT = cert_fingerprint
            LeapCertificate.LEAP_CERT = False

    @property
    def api_ca_bundle(self):
        return os.path.join(self._provider.config.leap_home, 'providers', self._server_name, 'keys', 'client', 'api.pem')

    def setup_ca_bundle(self):
        path = os.path.join(self._provider.config.leap_home, 'providers', self._server_name, 'keys', 'client')
        if not os.path.isdir(path):
            os.makedirs(path, 0700)
        self._download_cert(self.api_ca_bundle)

    def _download_cert(self, cert_file_name):
        cert = self._provider.fetch_valid_certificate()
        with open(cert_file_name, 'w') as file:
            file.write(cert)
