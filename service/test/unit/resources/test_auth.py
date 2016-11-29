from mockito import mock, when, any as ANY
from pixelated.resources.auth import SessionChecker, PixelatedRealm, PixelatedAuthSessionWrapper
from pixelated.resources.login_resource import LoginResource
from pixelated.resources.root_resource import RootResource
from test.unit.resources import DummySite
from twisted.cred import error
from twisted.cred.checkers import ANONYMOUS, AllowAnonymousAccess
from twisted.cred.portal import Portal
from twisted.internet.defer import succeed, fail
from twisted.python import failure
from twisted.trial import unittest
from twisted.web._auth.wrapper import UnauthorizedResource
from twisted.web.resource import IResource, getChildForRequest
from twisted.web.test.requesthelper import DummyRequest


class TestPixelatedRealm(unittest.TestCase):

    def setUp(self):
        self.authenticated_root_resource = mock()
        self.public_root_resource = mock()
        self.realm = PixelatedRealm(self.authenticated_root_resource, self.public_root_resource)

    def test_anonymous_user_gets_anonymous_resource(self):
        interface, avatar, logout_handler = self.realm.requestAvatar(ANONYMOUS, None, IResource)
        self.assertEqual(interface, IResource)
        self.assertIs(avatar, self.public_root_resource)

    def test_authenticated_user_gets_root_resource(self):
        interface, avatar, logout_handler = self.realm.requestAvatar('username', None, IResource)
        self.assertEqual(interface, IResource)
        self.assertIs(avatar, self.authenticated_root_resource)


class TestPixelatedAuthSessionWrapper(unittest.TestCase):

    def setUp(self):
        self.realm_mock = mock()
        services_factory = mock()
        session_checker = SessionChecker(services_factory)
        self.portal = Portal(self.realm_mock, [session_checker, AllowAnonymousAccess()])
        self.user_uuid_mock = mock()
        self.root_resource = RootResource(services_factory)
        self.anonymous_resource_mock = mock()

        self.session_wrapper = PixelatedAuthSessionWrapper(self.portal, self.root_resource, self.anonymous_resource_mock)
        self.request = DummyRequest([])
        self.request.prepath = ['']
        self.request.path = '/'

    def test_should_proxy_to_login_resource_when_the_user_is_not_logged_in(self):
        when(self.realm_mock).requestAvatar(ANONYMOUS, None, IResource).thenReturn((IResource, self.anonymous_resource_mock, lambda: None))

        deferred_resource = self.session_wrapper.getChildWithDefault('', self.request)
        d = deferred_resource.d

        def assert_anonymous_resource(resource):
            self.assertIs(resource, self.anonymous_resource_mock)

        d.addCallback(assert_anonymous_resource)
        return d

    def test_should_proxy_to_root_resource_when_the_user_is_logged_in(self):
        when(self.realm_mock).requestAvatar(ANY(), None, IResource).thenReturn((IResource, self.root_resource, lambda: None))

        deferred_resource = self.session_wrapper.getChildWithDefault('', self.request)
        d = deferred_resource.d

        def assert_root_resource(resource):
            self.assertIs(resource, self.root_resource)

        d.addCallback(assert_root_resource)
        return d

    def test_should_X_when_unauthenticated_user_requests_non_public_resource(self):
        when(self.realm_mock).requestAvatar(ANONYMOUS, None, IResource).thenReturn((IResource, self.anonymous_resource_mock, lambda: None))

        deferred_resource = self.session_wrapper.getChildWithDefault('', self.request)
        d = deferred_resource.d

        def assert_unauthorized_resource(resource):
            self.assertIs(resource, self.anonymous_resource_mock)

        d.addCallback(assert_unauthorized_resource)
        return d
