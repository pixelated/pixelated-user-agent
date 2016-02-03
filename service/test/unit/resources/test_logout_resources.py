from mock import patch
from mockito import mock, verify
from twisted.trial import unittest
from twisted.web.test.requesthelper import DummyRequest

from pixelated.resources.logout_resource import LogoutResource
from test.unit.resources import DummySite


class TestLogoutResource(unittest.TestCase):
    def setUp(self):
        self.services_factory = mock()
        self.resource = LogoutResource(self.services_factory)
        self.web = DummySite(self.resource)

    @patch('twisted.web.util.redirectTo')
    def test_logout(self, mock_redirect):
        request = DummyRequest(['/logout'])

        mock_redirect.return_value = 'haha'

        d = self.web.get(request)

        def expire_session_and_redirect(_):
            session = self.resource.get_session(request)
            self.assertFalse(session.is_logged_in())
            verify(self.services_factory).log_out_user(session.user_uuid)
            mock_redirect.assert_called_once_with('/login', request)

        d.addCallback(expire_session_and_redirect)
        return d
