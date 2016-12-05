from mockito import mock, when, any as ANY

from pixelated.application import get_static_folder
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
        self.root_resource = RootResource(services_factory, get_static_folder())
        self.anonymous_resource = RootResource(services_factory, get_static_folder(), public=True)

        self.session_wrapper = PixelatedAuthSessionWrapper(self.portal, self.root_resource, self.anonymous_resource)
        self.request = DummyRequest([])
        self.request.prepath = ['']
        self.request.path = '/'

    def test_root_url_should_delegate_to_public_root_resource_for_unauthenticated_user(self):
        when(self.realm_mock).requestAvatar(ANONYMOUS, None, IResource).thenReturn((IResource, self.anonymous_resource, lambda: None))
        request = DummyRequest([''])
        deferred_resource = getChildForRequest(self.session_wrapper, request)
        d = deferred_resource.d

        def assert_public_root_resource(resource):
            self.assertIs(resource, self.anonymous_resource)

        return d.addCallback(assert_public_root_resource)

    def test_root_url_should_delegate_to_protected_root_resource_for_authenticated_user(self):
        when(self.realm_mock).requestAvatar(ANY(), None, IResource).thenReturn((IResource, self.root_resource, lambda: None))
        request = DummyRequest([''])
        deferred_resource = getChildForRequest(self.session_wrapper, request)
        d = deferred_resource.d

        def assert_protected_root_resource(resource):
            self.assertIsInstance(resource, RootResource)

        return d.addCallback(assert_protected_root_resource)
