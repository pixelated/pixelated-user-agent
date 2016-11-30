from twisted.trial import unittest
from mockito import mock
from pixelated.resources.session import CSRF_TOKEN_LENGTH, PixelatedSession


class TestPixelatedSession(unittest.TestCase):

    def setUp(self):
        self.pixelated_session = PixelatedSession(mock())

    def test_csrf_token_should_be_configured_length(self):
        self.assertEqual(len(self.pixelated_session.get_csrf_token()), 2 * CSRF_TOKEN_LENGTH)

    def test_csrf_token_should_be_hexdigested(self):
        self.assertTrue(all(c in '0123456789abcdef' for c in self.pixelated_session.get_csrf_token()))

    def test_csrf_token_should_always_be_the_same_for_one_session(self):
        first_csrf_token = self.pixelated_session.get_csrf_token()
        second_csrf_token = self.pixelated_session.get_csrf_token()
        self.assertEqual(first_csrf_token, second_csrf_token)

    def test_csrf_token_should_be_different_for_different_session(self):
        first_csrf_token = self.pixelated_session.get_csrf_token()
        second_csrf_token = PixelatedSession(mock()).get_csrf_token()
        self.assertNotEqual(first_csrf_token, second_csrf_token)
