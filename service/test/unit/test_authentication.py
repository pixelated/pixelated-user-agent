from twisted.cred.error import UnauthorizedLogin
from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest

from leap.bitmask.bonafide._srp import SRPAuthError

from mock import patch, Mock

from pixelated.authentication import Authenticator
from pixelated.bitmask_libraries.provider import LeapProvider


PROVIDER_JSON = {
    "api_uri": "https://api.domain.org:4430",
    "api_version": "1",
    "ca_cert_fingerprint": "SHA256: some_stub_sha",
    "ca_cert_uri": "https://domain.org/ca.crt",
    "domain": "domain.org",
}


class AuthenticatorTest(unittest.TestCase):
    def setUp(self):
        with patch.object(LeapProvider, 'fetch_provider_json', return_value=PROVIDER_JSON):
            self._leap_provider = LeapProvider('domain.org')

    @inlineCallbacks
    def test_bonafide_srp_exceptions_should_raise_unauthorized_login(self):
        auth = Authenticator(self._leap_provider)
        mock_bonafide_session = Mock()
        mock_bonafide_session.authenticate = Mock(side_effect=SRPAuthError())
        with patch('pixelated.config.leap.Session', return_value=mock_bonafide_session):
            with self.assertRaises(UnauthorizedLogin):
                yield auth.authenticate('username', 'password')

    @inlineCallbacks
    def test_auth_username_with_domain_only_makes_bonafide_auth_with_username(self):
        auth = Authenticator(self._leap_provider)
        with patch('pixelated.authentication.authenticate') as mock_leap_authenticate:
            yield auth.authenticate('username@domain.org', 'password')
            mock_leap_authenticate.assert_called_once_with(self._leap_provider, 'username', 'password')

    def test_validate_username_accepts_username(self):
        auth = Authenticator(self._leap_provider)
        self.assertTrue(auth.validate_username('username'))

    def test_validate_username_accepts_email_address(self):
        auth = Authenticator(self._leap_provider)
        self.assertTrue(auth.validate_username('username@domain.org'))

    def test_validate_username_denies_other_domains(self):
        auth = Authenticator(self._leap_provider)
        self.assertFalse(auth.validate_username('username@wrongdomain.org'))

    def test_username_with_domain(self):
        auth = Authenticator(self._leap_provider)
        self.assertEqual('user@domain.org', auth.username_with_domain('user'))

    def test_extract_username_extracts_from_plain_username(self):
        auth = Authenticator(self._leap_provider)
        self.assertEqual(auth.extract_username('user'), 'user')

    def test_extract_username_extracts_from_email_address(self):
        auth = Authenticator(self._leap_provider)
        self.assertEqual(auth.extract_username('user@domain.org'), 'user')
