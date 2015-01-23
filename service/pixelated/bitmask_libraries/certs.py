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

from leap.common import ca_bundle

from .config import AUTO_DETECT_CA_BUNDLE

LEAP_CERT = None


def which_bundle(provider):
    if LEAP_CERT:
        return LEAP_CERT
    return str(LeapCertificate(provider).auto_detect_ca_bundle())


class LeapCertificate(object):
    def __init__(self, provider):
        self._config = provider.config
        self._server_name = provider.server_name
        self._certs_home = self._config.certs_home

    def auto_detect_ca_bundle(self):
        if self._config.ca_cert_bundle == AUTO_DETECT_CA_BUNDLE:
            local_cert = self._local_server_cert()
            if local_cert:
                return local_cert
            else:
                return ca_bundle.where()
        else:
            return self._config.ca_cert_bundle

    def _local_server_cert(self):
        cert_file = os.path.join(self._certs_home, '%s.ca.crt' % self._server_name)
        if os.path.isfile(cert_file):
            return cert_file
        else:
            return None
