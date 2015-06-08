import unittest

from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.config import AUTO_DETECT_CA_BUNDLE
from mock import MagicMock, patch


class CertsTest(unittest.TestCase):

    @patch('pixelated.bitmask_libraries.certs.os.path.isfile')
    @patch('pixelated.bitmask_libraries.certs.os.path.isdir')
    def test_that_which_bootstrap_cert_bundle_returns_string(self, mock_isdir, mock_isfile):
        mock_isfile.return_value = True
        mock_isdir.return_value = True
        config = MagicMock(bootstrap_ca_cert_bundle=AUTO_DETECT_CA_BUNDLE, leap_home='/leap/home')
        provider = MagicMock(server_name=u'test.leap.net', config=config)

        bundle = LeapCertificate(provider).auto_detect_bootstrap_ca_bundle()

        self.assertEqual('/leap/home/providers/test.leap.net/test.leap.net.ca.crt', bundle)

    @patch('pixelated.bitmask_libraries.certs.os.path.isfile')
    @patch('pixelated.bitmask_libraries.certs.os.path.isdir')
    def test_that_which_bundle_returns_string(self, mock_isdir, mock_isfile):
        mock_isfile.return_value = True
        mock_isdir.return_value = True

        config = MagicMock(bootstrap_ca_cert_bundle=AUTO_DETECT_CA_BUNDLE, ca_cert_bundle=None, leap_home='/some/leap/home')
        provider = MagicMock(server_name=u'test.leap.net', config=config)

        bundle = LeapCertificate(provider).api_ca_bundle()

        self.assertEqual('/some/leap/home/providers/test.leap.net/keys/client/api.pem', bundle)
