import os
import re

from mock import MagicMock, patch
from mockito import mock, when, any as ANY

import pixelated
from pixelated.application import UserAgentMode, get_static_folder
from pixelated.resources import IPixelatedSession, UnAuthorizedResource
from pixelated.resources.features_resource import FeaturesResource
from pixelated.resources.login_resource import LoginResource
from test.unit.resources import DummySite
from twisted.cred.checkers import ANONYMOUS
from twisted.internet.defer import succeed
from twisted.trial import unittest
from twisted.web.resource import IResource, getChildForRequest
from twisted.web.static import File
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.root_resource import InboxResource, RootResource, MODE_STARTUP, MODE_RUNNING


class TestPublicRootResource(unittest.TestCase):

    def setUp(self):
        self.public_root_resource = RootResource(mock(), get_static_folder(), public=True)
        self.web = DummySite(self.public_root_resource)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_put_child_public_adds_resource(self, *mocks):
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        url_fragment, resource_mock = 'some-url-fragment', mock()
        self.public_root_resource.putChildPublic(url_fragment, resource_mock)
        request = DummyRequest([url_fragment])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.public_root_resource, request)
        self.assertIs(child_resource, resource_mock)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_put_child_protected_adds_unauthorized(self, *mocks):
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        url_fragment, resource_mock = 'some-url-fragment', mock()
        self.public_root_resource.putChildProtected(url_fragment, resource_mock)
        request = DummyRequest([url_fragment])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.public_root_resource, request)
        self.assertIsInstance(child_resource, UnAuthorizedResource)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_put_child_adds_unauthorized(self, *mocks):
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        url_fragment, resource_mock = 'some-url-fragment', mock()
        self.public_root_resource.putChild(url_fragment, resource_mock)
        request = DummyRequest([url_fragment])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.public_root_resource, request)
        self.assertIsInstance(child_resource, UnAuthorizedResource)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_private_resource_returns_401(self, *mocks):
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        request = DummyRequest(['mails'])
        request.addCookie = MagicMock(return_value='stubbed')
        d = self.web.get(request)

        def assert_unauthorized(request):
            self.assertEqual(401, request.responseCode)
            self.assertEqual("Unauthorized!", request.written[0])

        d.addCallback(assert_unauthorized)
        return d

    @patch('pixelated.resources.mails_resource.events.register')
    def test_login_url_should_delegate_to_login_resource(self, *mocks):
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        request = DummyRequest(['login'])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.public_root_resource, request)
        self.assertIsInstance(child_resource, LoginResource)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_root_url_should_redirect_to_login_resource(self, *mocks):
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        request = DummyRequest([''])
        request.addCookie = MagicMock(return_value='stubbed')
        d = self.web.get(request)

        def assert_redirect(request):
            self.assertEqual(302, request.responseCode)
            self.assertEqual(["login"], request.responseHeaders.getRawHeaders('location', [None]))

        d.addCallback(assert_redirect)
        return d


class TestRootResource(unittest.TestCase):
    MAIL_ADDRESS = 'test_user@pixelated-project.org'

    def setUp(self):
        self.mail_service = mock()
        self.services_factory = mock()
        self.services_factory.mode = UserAgentMode(is_single_user=True)
        self.services = mock()
        self.services.mail_service = self.mail_service
        self.services_factory._services_by_user = {'someuserid': self.mail_service}
        when(self.services_factory).services(ANY()).thenReturn(self.services)
        self.mail_service.account_email = self.MAIL_ADDRESS

        self.root_resource = RootResource(self.services_factory, get_static_folder())
        self.web = DummySite(self.root_resource)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_put_child_protected_adds_resource(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())
        url_fragment, resource_mock = 'some-url-fragment', mock()
        self.root_resource.putChildProtected(url_fragment, resource_mock)
        request = DummyRequest([url_fragment])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.root_resource, request)
        self.assertIs(child_resource, resource_mock)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_put_child_adds_resource(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())
        url_fragment, resource_mock = 'some-url-fragment', mock()
        self.root_resource.putChild(url_fragment, resource_mock)
        request = DummyRequest([url_fragment])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.root_resource, request)
        self.assertIs(child_resource, resource_mock)

    def test_root_url_should_delegate_to_inbox(self):
        request = DummyRequest([''])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.root_resource, request)
        self.assertIsInstance(child_resource, InboxResource)

    @patch('pixelated.resources.mails_resource.events.register')
    def test_login_url_should_delegate_to_login_resource(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())
        request = DummyRequest(['login'])
        request.addCookie = MagicMock(return_value='stubbed')
        child_resource = getChildForRequest(self.root_resource, request)
        self.assertIsInstance(child_resource, LoginResource)

    def _test_should_renew_xsrf_cookie(self):
        request = DummyRequest([''])
        request.addCookie = MagicMock(return_value='stubbed')
        generated_csrf_token = 'csrf_token'
        mock_sha = MagicMock()
        mock_sha.hexdigest = MagicMock(return_value=generated_csrf_token)

        with patch('hashlib.sha256', return_value=mock_sha):
            d = self.web.get(request)

        def assert_csrf_cookie(_):
            request.addCookie.assert_called_once_with('XSRF-TOKEN', generated_csrf_token)

        d.addCallback(assert_csrf_cookie)
        return d

    def test_should_renew_xsrf_cookie_on_startup_mode(self):
        self.root_resource._mode = MODE_STARTUP
        self._test_should_renew_xsrf_cookie()

    def test_should_renew_xsrf_cookie_on_running_mode(self):
        self.root_resource._mode = MODE_RUNNING
        self._test_should_renew_xsrf_cookie()

    def test_should_unavailable_child_resource_during_startup(self):
        self.root_resource._mode = MODE_STARTUP

        request = DummyRequest(['/child'])
        request.addCookie = MagicMock(return_value='stubbed')
        request.getCookie = MagicMock(return_value='irrelevant -- stubbed')

        d = self.web.get(request)

        def assert_unavailable(_):
            self.assertEqual(503, request.responseCode)
            self.assertEqual("Service Unavailable", request.written[0])

        d.addCallback(assert_unavailable)
        return d

    def _mock_ajax_csrf(self, request, csrf_token):
        request.requestHeaders.setRawHeaders('x-requested-with', ['XMLHttpRequest'])
        request.requestHeaders.setRawHeaders('x-xsrf-token', [csrf_token])

    @patch('pixelated.resources.mails_resource.events.register')
    def test_should_unauthorize_child_resource_ajax_requests_when_csrf_mismatch(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['/child'])
        request.addCookie = MagicMock(return_value='stubbed')
        request.method = 'POST'
        self._mock_ajax_csrf(request, 'stubbed csrf token')

        request.getCookie = MagicMock(return_value='mismatched csrf token')

        d = self.web.get(request)

        def assert_unauthorized(_):
            self.assertEqual(401, request.responseCode)
            self.assertEqual("Unauthorized!", request.written[0])

        d.addCallback(assert_unauthorized)
        return d

    def test_GET_should_return_503_for_uninitialized_resource(self):
        request = DummyRequest(['/sandbox/'])
        request.addCookie = MagicMock(return_value='stubbed')
        request.method = 'GET'

        request.getCookie = MagicMock(return_value='stubbed csrf token')

        d = self.web.get(request)

        def assert_unavailable(_):
            self.assertEqual(503, request.responseCode)

        d.addCallback(assert_unavailable)
        return d

    @patch('pixelated.resources.mails_resource.events.register')
    def test_GET_should_return_404_for_non_existing_resource(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['non-existing-child'])
        request.addCookie = MagicMock(return_value='stubbed')
        request.method = 'GET'
        request.getCookie = MagicMock(return_value='stubbed csrf token')

        d = self.web.get(request)

        def assert_not_found(_):
            self.assertEqual(404, request.responseCode)

        d.addCallback(assert_not_found)
        return d

    @patch('pixelated.resources.mails_resource.events.register')
    def test_should_404_non_existing_resource_with_valid_csrf(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['non-existing-child'])
        request.addCookie = MagicMock(return_value='stubbed')
        request.method = 'POST'
        self._mock_ajax_csrf(request, 'stubbed csrf token')
        request.getCookie = MagicMock(return_value='stubbed csrf token')

        d = self.web.get(request)

        def assert_not_found(_):
            self.assertEqual(404, request.responseCode)
            self.assertIn("No Such Resource", request.written[0])

        d.addCallback(assert_not_found)
        return d

    def test_should_authorize_child_resource_non_ajax_GET_requests(self):
        request = DummyRequest(['features'])
        request.addCookie = MagicMock(return_value='stubbed')

        request.getCookie = MagicMock(return_value='irrelevant -- stubbed')
        self.root_resource.putChild('features', FeaturesResource())
        self.root_resource._mode = MODE_RUNNING

        d = self.web.get(request)

        def assert_unauthorized(_):
            self.assertEqual(200, request.code)

        d.addCallback(assert_unauthorized)
        return d

    @patch('pixelated.resources.mails_resource.events.register')
    def test_should_unauthorize_child_resource_non_ajax_POST_requests_when_csrf_input_mismatch(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['mails'])
        request.method = 'POST'
        request.addArg('csrftoken', 'some csrf token')
        mock_content = MagicMock()
        mock_content.read = MagicMock(return_value={})
        request.content = mock_content

        request.addCookie = MagicMock(return_value='stubbed')
        request.getCookie = MagicMock(return_value='mismatched csrf token')

        d = self.web.get(request)

        def assert_unauthorized(_):
            self.assertEqual(401, request.responseCode)
            self.assertEqual("Unauthorized!", request.written[0])

        d.addCallback(assert_unauthorized)
        return d

    @patch('pixelated.resources.mails_resource.events.register')
    def test_assets_should_be_publicly_available(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['static', 'dummy.json'])
        request.addCookie = MagicMock(return_value='stubbed')
        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(200, request.responseCode)

        d.addCallback(assert_response)
        return d

    @patch('pixelated.resources.mails_resource.events.register')
    def test_login_should_be_publicly_available(self, *mocks):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['login'])
        request.addCookie = MagicMock(return_value='stubbed')
        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(200, request.responseCode)

        d.addCallback(assert_response)
        return d

    def test_root_should_be_handled_by_inbox_resource(self):
        request = DummyRequest([])
        request.addCookie = MagicMock(return_value='stubbed')
        request.prepath = ['']
        request.path = '/'
        # TODO: setup mocked portal

        resource = self.root_resource.getChildWithDefault(request.prepath[-1], request)
        self.assertIsInstance(resource, InboxResource)

    def test_inbox_should_not_be_public(self):
        request = DummyRequest([])
        request.addCookie = MagicMock(return_value='stubbed')
        request.prepath = ['']
        request.path = '/'
        # TODO: setup mocked portal

        resource = self.root_resource.getChildWithDefault(request.prepath[-1], request)
        self.assertIsInstance(resource, InboxResource)

    def test_every_url_should_get_csrftoken_header(self):
        # self.root_resource.initialize(provider=mock(), authenticator=mock())
        request = DummyRequest(['any'])
        request.addCookie = MagicMock(return_value='stubbed')
        d = self.web.get(request)

        def assert_add_cookie_called_for_csrftoken(request):
            csrftoken = IPixelatedSession(request.getSession()).get_csrf_token()
            self.assertEqual([(('XSRF-TOKEN', csrftoken),)], request.addCookie.call_args_list)

        d.addCallback(assert_add_cookie_called_for_csrftoken)
        return d
