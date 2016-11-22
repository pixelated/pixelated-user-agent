from mockito import mock, when, any as ANY
from pixelated.resources.auth import PixelatedAuthSessionWrapper
from pixelated.resources.login_resource import LoginResource
from pixelated.resources.root_resource import RootResource
from test.unit.resources import DummySite
from twisted.cred.checkers import ANONYMOUS
from twisted.internet.defer import succeed
from twisted.trial import unittest
from twisted.web.resource import IResource
from twisted.web.test.requesthelper import DummyRequest


class TestPixelatedAuthSessionWrapper(unittest.TestCase):

    def setUp(self):
        self.portal_mock = mock()
        self.user_uuid_mock = mock()
        self.root_resource_mock = mock()
        self.anonymous_resource_mock = mock()
        credential_factories_mock = mock()

        self.session_wrapper = PixelatedAuthSessionWrapper(self.portal_mock, self.root_resource_mock, self.anonymous_resource_mock, credential_factories_mock)
        self.request = DummyRequest([])
        self.request.prepath = ['']
        self.request.path = '/'

    def test_should_proxy_to_login_resource_when_the_user_is_not_logged_in(self):
        when(self.portal_mock).login(ANY(), None, IResource).thenReturn(succeed((IResource, ANONYMOUS, lambda: None)))

        deferred_resource = self.session_wrapper.getChildWithDefault('/', self.request)
        d = deferred_resource.d

        def assert_anonymous_resource(resource):
            self.assertIs(resource, self.anonymous_resource_mock)

        d.addCallback(assert_anonymous_resource)
        return d

    def test_should_proxy_to_root_resource_when_the_user_is_logged_in(self):
        when(self.portal_mock).login(ANY(), None, IResource).thenReturn(succeed((IResource, self.user_uuid_mock, lambda: None)))

        deferred_resource = self.session_wrapper.getChildWithDefault('/', self.request)
        d = deferred_resource.d

        def assert_root_resource(resource):
            self.assertIs(resource, self.root_resource_mock)

        d.addCallback(assert_root_resource)
        return d
