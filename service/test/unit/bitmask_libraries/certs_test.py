import unittest

from pixelated.bitmask_libraries.certs import which_bundle
from pixelated.bitmask_libraries.config import AUTO_DETECT_CA_BUNDLE
from mock import MagicMock, patch


class CertsTest(unittest.TestCase):

    @patch('pixelated.bitmask_libraries.certs.os.path.isfile')
    def test_that_which_bundle_returns_byte_string(self, mock_isfile):
        mock_isfile.return_value = True
        config = MagicMock(ca_cert_bundle=AUTO_DETECT_CA_BUNDLE, certs_home='/some/path')
        provider = MagicMock(server_name=u'test.leap.net', config=config)

        bundle = which_bundle(provider)

        self.assertEqual('/some/path/test.leap.net.ca.crt', bundle)
        self.assertEqual(str, type(bundle))
