import os

from leap.common import ca_bundle

from .config import AUTO_DETECT_CA_BUNDLE


def which_bundle(provider):
    return LeapCertificate(provider).auto_detect_ca_bundle()


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
