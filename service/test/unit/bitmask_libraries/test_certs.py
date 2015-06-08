import unittest

from pixelated.bitmask_libraries.certs import LeapCertificate
from mock import MagicMock, patch


class CertsTest(unittest.TestCase):

    def test_set_cert_and_fingerprint_sets_cert(self):
        LeapCertificate.set_cert_and_fingerprint('some cert', None)

        self.assertIsNone(LeapCertificate.LEAP_FINGERPRINT)
        self.assertEqual('some cert', LeapCertificate.LEAP_CERT)

    def test_set_cert_and_fingerprint_sets_fingerprint(self):
        LeapCertificate.set_cert_and_fingerprint(None, 'fingerprint')

        self.assertEqual('fingerprint', LeapCertificate.LEAP_FINGERPRINT)
        self.assertFalse(LeapCertificate.LEAP_CERT)

    def test_api_ca_bundle(self):
        config = MagicMock(leap_home='/some/leap/home')
        provider = MagicMock(server_name=u'test.leap.net', config=config)

        cert = LeapCertificate(provider).api_ca_bundle

        self.assertEqual('/some/leap/home/providers/test.leap.net/keys/client/api.pem', cert)
