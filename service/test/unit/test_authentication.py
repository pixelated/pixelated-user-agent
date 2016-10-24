from twisted.trial import unittest

from pixelated.authentication import Authenticator


class AuthenticatorTest(unittest.TestCase):
    def test_authenticates_with_username_and_password(self):
        self.fail()

    def test_validate_username_accepts_username(self):
        auth = Authenticator('domain.org')
        self.assertTrue(auth.validate_username('username'))

    def test_validate_username_accepts_email_address(self):
        auth = Authenticator('domain.org')
        self.assertTrue(auth.validate_username('username@domain.org'))

    def test_validate_username_denies_other_domains(self):
        auth = Authenticator('domain.org')
        self.assertFalse(auth.validate_username('username@wrongdomain.org'))

    def test_username_with_domain(self):
        auth = Authenticator('domain.org')
        self.assertEqual('user@domain.org', auth.username_with_domain('user'))

    def test_extract_username_extracts_from_plain_username(self):
        auth = Authenticator('domain.org')
        self.assertEqual(auth.extract_username('user'), 'user')

    def test_extract_username_extracts_from_email_address(self):
        auth = Authenticator('domain.org')
        self.assertEqual(auth.extract_username('user@domain.org'), 'user')
