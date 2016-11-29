import os
import re

from mock import MagicMock, patch
from mockito import mock, when, any as ANY

import pixelated
from pixelated.application import UserAgentMode
from pixelated.resources.features_resource import FeaturesResource
from pixelated.resources.login_resource import LoginResource
from test.unit.resources import DummySite
from twisted.cred.checkers import ANONYMOUS
from twisted.internet.defer import succeed
from twisted.trial import unittest
from twisted.web.resource import IResource, getChildForRequest
from twisted.web.static import File
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.root_resource import InboxResource, PublicRootResource, RootResource, MODE_STARTUP, MODE_RUNNING


class TestPublicRootResource(unittest.TestCase):
    pass


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

        root_resource = RootResource(self.services_factory)
        self.web = DummySite(root_resource)
        self.root_resource = root_resource

    def test_root_url_should_delegate_to_inbox(self):
        request = DummyRequest([''])
        request.addCookie = lambda key, value: 'stubbed'
        child_resource = getChildForRequest(self.root_resource, request)
        self.assertIsInstance(child_resource, InboxResource)

    def test_login_url_should_delegate_to_login_resource(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())
        request = DummyRequest(['login'])
        request.addCookie = lambda key, value: 'stubbed'
        child_resource = getChildForRequest(self.root_resource, request)
        self.assertIsInstance(child_resource, LoginResource)

    def _test_should_renew_xsrf_cookie(self):
        request = DummyRequest([''])
        request.addCookie = MagicMock()
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

    def test_should_unauthorize_child_resource_ajax_requests_when_csrf_mismatch(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['/child'])
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
        request.method = 'GET'

        request.getCookie = MagicMock(return_value='stubbed csrf token')

        d = self.web.get(request)

        def assert_unavailable(_):
            self.assertEqual(503, request.responseCode)

        d.addCallback(assert_unavailable)
        return d

    def test_GET_should_return_404_for_non_existing_resource(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['/non-existing-child'])
        request.method = 'GET'
        request.getCookie = MagicMock(return_value='stubbed csrf token')

        d = self.web.get(request)

        def assert_not_found(_):
            self.assertEqual(404, request.responseCode)

        d.addCallback(assert_not_found)
        return d

    def test_should_404_non_existing_resource_with_valid_csrf(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['/non-existing-child'])
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

        request.getCookie = MagicMock(return_value='irrelevant -- stubbed')
        self.root_resource.putChild('features', FeaturesResource())
        self.root_resource._mode = MODE_RUNNING

        d = self.web.get(request)

        def assert_unauthorized(_):
            self.assertEqual(200, request.code)

        d.addCallback(assert_unauthorized)
        return d

    def test_should_unauthorize_child_resource_non_ajax_POST_requests_when_csrf_input_mismatch(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['mails'])
        request.method = 'POST'
        request.addArg('csrftoken', 'some csrf token')
        mock_content = MagicMock()
        mock_content.read = MagicMock(return_value={})
        request.content = mock_content

        request.getCookie = MagicMock(return_value='mismatched csrf token')

        d = self.web.get(request)

        def assert_unauthorized(_):
            self.assertEqual(401, request.responseCode)
            self.assertEqual("Unauthorized!", request.written[0])

        d.addCallback(assert_unauthorized)
        return d

    def test_assets_should_be_publicly_available(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['assets', 'dummy.json'])
        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(200, request.responseCode)

        d.addCallback(assert_response)
        return d

    def test_login_should_be_publicly_available(self):
        self.root_resource.initialize(provider=mock(), authenticator=mock())

        request = DummyRequest(['login'])
        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(200, request.responseCode)

        d.addCallback(assert_response)
        return d

    def test_root_should_be_handled_by_inbox_resource(self):
        request = DummyRequest([])
        request.prepath = ['']
        request.path = '/'
        # TODO: setup mocked portal

        resource = self.root_resource.getChildWithDefault(request.prepath[-1], request)
        self.assertIsInstance(resource, InboxResource)

    def test_inbox_should_not_be_public(self):
        request = DummyRequest([])
        request.prepath = ['']
        request.path = '/'
        # TODO: setup mocked portal

        resource = self.root_resource.getChildWithDefault(request.prepath[-1], request)
        self.assertIsInstance(resource, InboxResource)
