from mock import patch, MagicMock
from twisted.trial import unittest
from twisted.internet import defer
from twisted.web.error import UnsupportedMethod
from twisted.web.test.requesthelper import DummyRequest

from pixelated.resources.logout_resource import LogoutResource
from test.unit.resources import DummySite


class TestLogoutResource(unittest.TestCase):
    def setUp(self):
        self.services_factory = MagicMock()
        self.resource = LogoutResource(self.services_factory)
        self.services_factory.log_out_user.return_value = defer.succeed(None)
        self.web = DummySite(self.resource)

    @patch('twisted.web.util.redirectTo')
    def test_logout(self, mock_redirect):
        request = DummyRequest(['/logout'])
        request.method = 'POST'

        session = self.resource.get_session(request)
        session.expire = MagicMock()
        mock_redirect.return_value = 'some redirect response'

        d = self.web.get(request)

        def expire_session_and_redirect(_):
            session = self.resource.get_session(request)
            self.services_factory.log_out_user.assert_called_once_with(session.user_uuid)
            session.expire.assert_called_once_with()
            mock_redirect.assert_called_once_with('/login', request)

        d.addCallback(expire_session_and_redirect)
        return d

    def test_get_is_not_supported_for_logout(self):
        request = DummyRequest(['/logout'])
        request.method = 'GET'

        self.assertRaises(UnsupportedMethod, self.web.get, request)
