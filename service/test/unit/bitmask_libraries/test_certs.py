import unittest

from pixelated.bitmask_libraries.certs import LeapCertificate
from mock import MagicMock, patch


class CertsTest(unittest.TestCase):

    def setUp(self):
        config = MagicMock(leap_home='/some/leap/home')
        self.provider = MagicMock(server_name=u'test.leap.net', config=config)

    def test_set_cert_and_fingerprint_sets_cert(self):
        LeapCertificate.set_cert_and_fingerprint('some cert', None)

        certs = LeapCertificate(self.provider)

        self.assertIsNone(certs.LEAP_FINGERPRINT)
        self.assertEqual('some cert', certs.provider_web_cert)

    def test_set_cert_and_fingerprint_sets_fingerprint(self):
        LeapCertificate.set_cert_and_fingerprint(None, 'fingerprint')

        certs = LeapCertificate(self.provider)

        self.assertEqual('fingerprint', LeapCertificate.LEAP_FINGERPRINT)
        self.assertFalse(certs.provider_web_cert)

    def test_provider_api_cert(self):
        certs = LeapCertificate(self.provider).provider_api_cert

        self.assertEqual('/some/leap/home/providers/test.leap.net/keys/client/api.pem', certs)
