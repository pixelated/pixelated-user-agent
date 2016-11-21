import unittest

from mockito import mock

from test.unit.resources import DummySite
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.auth import PixelatedAuthSessionWrapper


class TestRootResource(unittest.TestCase):

    def setUp(self):
        self.portal = mock()
        self.mock_root_resource = mock()
        self.anonymous_resource = mock()
        self.credential_factories = mock()

        self.session_wrapper = PixelatedAuthSessionWrapper(self.portal, self.mock_root_resource, self.anonymous_resource, self.credential_factories)
        self.web = DummySite(self.session_wrapper)

    def test_should_use_login_resource_when_the_user_is_not_logged_in (self):
        request = DummyRequest([''])
        self.session_wrapper.getChildWithDefault('/', request)

        def assert_response(_):
            self.assertEquals(len(matches), 1)

        d.addCallback(assert_response)
        return d

