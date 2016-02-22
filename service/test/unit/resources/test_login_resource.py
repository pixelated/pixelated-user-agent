import os

import test.support.mockito

from leap.exceptions import SRPAuthenticationError
from mock import patch
from mockito import mock, when, any as ANY, verify, verifyZeroInteractions, verifyNoMoreInteractions
from twisted.trial import unittest
from twisted.web.resource import IResource
from twisted.web.test.requesthelper import DummyRequest

from pixelated.bitmask_libraries.session import LeapSession, LeapSessionFactory
from pixelated.resources.login_resource import LoginResource
from test.unit.resources import DummySite


class TestLoginResource(unittest.TestCase):
    def setUp(self):
        self.services_factory = mock()
        self.portal = mock()
        self.resource = LoginResource(self.services_factory, self.portal)
        self.web = DummySite(self.resource)

    def test_children_resources_are_unauthorized_when_not_logged_in(self):
        request = DummyRequest(['/some_child_resource'])

        d = self.web.get(request)

        def assert_unauthorized_resources(_):
            self.assertEqual(401, request.responseCode)
            self.assertEqual("Unauthorized!", request.written[0])

        d.addCallback(assert_unauthorized_resources)
        return d

    @patch('pixelated.resources.session.PixelatedSession.is_logged_in')
    def test_there_are_no_grand_children_resources_when_logged_in(self, mock_is_logged_in):
        request = DummyRequest(['/login/grand_children'])
        mock_is_logged_in.return_value = True
        when(self.services_factory).is_logged_in(ANY()).thenReturn(True)

        d = self.web.get(request)

        def assert_resources_not_found(_):
            self.assertEqual(404, request.responseCode)
            self.assertIn("No Such Resource", request.written[0])

        d.addCallback(assert_resources_not_found)
        return d

    def test_get(self):
        request = DummyRequest([''])

        d = self.web.get(request)

        def assert_form_rendered(_):
            self.assertEqual(200, request.responseCode)
            form_action = 'action="/login"'
            form_method = 'method="post"'
            input_username = 'name="username"'
            input_password = 'name="password"'
            input_submit = 'name="login"'
            default_disclaimer = 'Some disclaimer'
            written_response = ''.join(request.written)
            self.assertIn(form_action, written_response)
            self.assertIn(form_method, written_response)
            self.assertIn(input_password, written_response)
            self.assertIn(input_submit, written_response)
            self.assertIn(input_username, written_response)
            self.assertIn(default_disclaimer, written_response)

        d.addCallback(assert_form_rendered)
        return d

    def _write(self, filename, content):
        with open(filename, 'w') as disclaimer_file:
            disclaimer_file.write(content)

    def test_override_login_disclaimer_message(self):
        request = DummyRequest([''])

        banner_file_name = 'banner.txt'
        banner_disclaimer_content = '<p>some custom disclaimer</p>'
        self._write(banner_file_name, banner_disclaimer_content)

        self.resource._disclaimer_banner = 'service/_trial_temp/' + banner_file_name

        d = self.web.get(request)

        def assert_custom_disclaimer_rendered(_):
            self.assertEqual(200, request.responseCode)
            written_response = ''.join(request.written)
            self.assertIn(banner_disclaimer_content, written_response)

        def tear_down(_):
            os.remove(banner_file_name)

        d.addCallback(assert_custom_disclaimer_rendered)
        d.addCallback(tear_down)
        return d

    def test_non_xml_compliant_banner_will_send_default_invalid_format_banner(self):
        request = DummyRequest([''])

        banner_file_name = 'banner.txt'
        xml_invalid_banner = '<p>some unclosed paragraph'
        self._write(banner_file_name, xml_invalid_banner)

        self.resource._disclaimer_banner = 'service/_trial_temp/' + banner_file_name

        d = self.web.get(request)

        def assert_default_invalid_banner_disclaimer_rendered(_):
            self.assertEqual(200, request.responseCode)
            written_response = ''.join(request.written)
            self.assertIn("Invalid XML template format for service/_trial_temp/banner.txt.", written_response)

        def tear_down(_):
            os.remove(banner_file_name)

        d.addCallback(assert_default_invalid_banner_disclaimer_rendered)
        d.addCallback(tear_down)
        return d


class TestLoginPOST(unittest.TestCase):
    def setUp(self):
        self.services_factory = mock()
        self.portal = mock()
        self.provider = mock()
        self.resource = LoginResource(self.services_factory, self.portal)
        self.web = DummySite(self.resource)

        self.request = DummyRequest([''])
        username = 'ayoyo'
        self.request.addArg('username', username)
        password = 'ayoyo_password'
        self.username = username
        self.password = password
        self.request.addArg('password', password)
        self.request.method = 'POST'
        leap_session = mock(LeapSession)
        user_auth = mock()
        user_auth.uuid = 'some_user_uuid'
        leap_session.user_auth = user_auth
        config = mock()
        config.leap_home = 'some_folder'
        leap_session.config = config
        leap_session.fresh_account = False
        self.leap_session = leap_session
        self.user_auth = user_auth

    def mock_user_has_services_setup(self):
        when(self.services_factory).is_logged_in('some_user_uuid').thenReturn(True)

    def test_login_responds_interstitial_and_add_corresponding_session_to_services_factory(self):
        irrelevant = None
        when(self.portal).login(ANY(), None, IResource).thenReturn((irrelevant, self.leap_session, irrelevant))
        when(self.services_factory).create_services_from(self.leap_session).thenAnswer(self.mock_user_has_services_setup)

        d = self.web.get(self.request)

        def assert_login_setup_service_for_user(_):
            verify(self.portal).login(ANY(), None, IResource)
            verify(self.services_factory).create_services_from(self.leap_session)
            interstitial_js_in_template = '<script src="startup-assets/Interstitial.js"></script>'
            self.assertIn(interstitial_js_in_template, self.request.written[0])
            self.assertTrue(self.resource.is_logged_in(self.request))

        d.addCallback(assert_login_setup_service_for_user)
        return d

    def test_login_does_not_reload_services_if_already_loaded(self):
        irrelevant = None
        when(self.portal).login(ANY(), None, IResource).thenReturn((irrelevant, self.leap_session, irrelevant))
        when(self.services_factory).is_logged_in('some_user_uuid').thenReturn(True)

        d = self.web.get(self.request)

        def assert_login_setup_service_for_user(_):
            verify(self.portal).login(ANY(), None, IResource)
            verify(self.services_factory).is_logged_in('some_user_uuid')
            verifyNoMoreInteractions(self.services_factory)
            interstitial_js_in_template = '<script src="startup-assets/Interstitial.js"></script>'
            self.assertIn(interstitial_js_in_template, self.request.written[0])
            self.assertTrue(self.resource.is_logged_in(self.request))

        d.addCallback(assert_login_setup_service_for_user)
        return d

    def test_should_return_form_back_with_error_message_when_login_fails(self):
        when(self.portal).login(ANY(), None, IResource).thenRaise(Exception())
        d = self.web.get(self.request)

        def assert_login_setup_service_for_user(_):
            verify(self.portal).login(ANY(), None, IResource)
            self.assertEqual(401, self.request.responseCode)
            written_response = ''.join(self.request.written)
            self.assertIn('Invalid credentials', written_response)
            self.assertFalse(self.resource.is_logged_in(self.request))

        d.addCallback(assert_login_setup_service_for_user)
        return d

    @patch('pixelated.bitmask_libraries.session.LeapSessionFactory.create')
    @patch('leap.auth.SRPAuth.authenticate')
    @patch('pixelated.config.services.Services.setup')
    def test_leap_session_is_not_created_when_leap_auth_fails(self, mock_service_setup, mock_leap_srp_auth, mock_leap_session_create):
        mock_leap_srp_auth.side_effect = SRPAuthenticationError()

        d = self.web.get(self.request)

        def assert_login_setup_service_for_user(_):
            verify(self.portal).login(ANY(), None, IResource)
            self.assertFalse(mock_leap_session_create.called)
            self.assertFalse(mock_service_setup.called)
            self.assertEqual(401, self.request.responseCode)
            self.assertFalse(self.resource.is_logged_in(self.request))

        d.addCallback(assert_login_setup_service_for_user)
        return d

    @patch('twisted.web.util.redirectTo')
    @patch('pixelated.resources.session.PixelatedSession.is_logged_in')
    def test_should_not_process_login_if_already_logged_in(self, mock_logged_in, mock_redirect):
        mock_logged_in.return_value = True
        when(self.services_factory).is_logged_in(ANY()).thenReturn(True)
        mock_redirect.return_value = "mocked redirection"
        when(self.portal).login(ANY(), None, IResource).thenRaise(Exception())
        d = self.web.get(self.request)

        def assert_login_setup_service_for_user(_):
            verifyZeroInteractions(self.portal)
            mock_redirect.assert_called_once_with('/', self.request)

        d.addCallback(assert_login_setup_service_for_user)
        return d
