import unittest

from leap.common.events import catalog as events
from mock import patch, MagicMock, ANY
import pixelated


class ApplicationTest(unittest.TestCase):

    class MockConfig:
        def __init__(self, port, host, sslkey=None, sslcert=None):
            self.port = port
            self.host = host
            self.sslkey = sslkey
            self.sslcert = sslcert
            self.home = 'leap_home'

    @patch('leap.common.events.client')
    @patch('pixelated.application.reactor')
    def test_that_start_site_binds_to_tcp_port_if_no_ssl_options(self, reactor_mock, _):
        app_mock = MagicMock()
        config = ApplicationTest.MockConfig(12345, '127.0.0.1')

        pixelated.application.start_site(config, app_mock)

        reactor_mock.listenTCP.assert_called_once_with(12345, ANY, interface='127.0.0.1')

    @patch('leap.common.events.client')
    @patch('pixelated.application.reactor')
    def test_that_start_site_binds_to_ssl_if_ssl_options(self, reactor_mock, _):
        app_mock = MagicMock()
        pixelated.application._ssl_options = lambda x, y: 'options'

        config = ApplicationTest.MockConfig(12345, '127.0.0.1', sslkey="sslkey", sslcert="sslcert")

        pixelated.application.start_site(config, app_mock)

        reactor_mock.listenSSL.assert_called_once_with(12345, ANY, 'options', interface='127.0.0.1')

    @patch('leap.common.events.client')
    @patch('pixelated.application.reactor')
    @patch('pixelated.application.services.Services')
    def test_that_start_user_agent_binds_to_tcp_port_if_no_ssl_options(self, services_mock, reactor_mock, _):
        # FIXME patch something closer, instead of leap.common
        app_mock = MagicMock()
        services_factory_mock = MagicMock()
        leap_session = MagicMock()
        config = ApplicationTest.MockConfig(12345, '127.0.0.1', leap_session)

        d = pixelated.application.start_user_agent_in_single_user_mode(app_mock, services_factory_mock, config.home, leap_session)

        def _assert(_):
            services_mock.assert_called_once_with(leap_session)

        d.addCallback(_assert)
        return d

    @patch('leap.common.events.client')
    @patch('pixelated.application.reactor')
    @patch('pixelated.application.services.Services')
    def test_that_start_user_agent_binds_to_ssl_if_ssl_options(self, services_mock, reactor_mock, _):
        # FIXME patch something closer, instead of leap.common
        app_mock = MagicMock()
        services_factory_mock = MagicMock()
        leap_session = MagicMock()
        pixelated.application._ssl_options = lambda x, y: 'options'

        config = ApplicationTest.MockConfig(12345, '127.0.0.1', sslkey="sslkey", sslcert="sslcert")

        d = pixelated.application.start_user_agent_in_single_user_mode(app_mock, services_factory_mock, config.home, leap_session)

        def _assert(_):
            services_mock.assert_called_once_with(leap_session)

        d.addCallback(_assert)
        return d

    @patch('leap.common.events.client')
    @patch('pixelated.application.reactor')
    @patch('pixelated.application.services.Services')
    def test_should_log_user_out_if_invalid_soledad_token(self, services_mock, reactor_mock, events_mock):
        app_mock = MagicMock()
        services_factory_mock = MagicMock()

        mock_service_log_user_out = MagicMock(return_value=None)
        services_factory_mock.log_out_user = mock_service_log_user_out

        leap_session = MagicMock()
        register_mock = events_mock.register
        register_mock.register.return_value = None

        config = ApplicationTest.MockConfig(12345, '127.0.0.1')
        d = pixelated.application.start_user_agent_in_single_user_mode(app_mock, services_factory_mock, config.home, leap_session)

        pixelated.application.add_top_level_system_callbacks(d, services_factory_mock)

        def _assert_user_logged_out_using_uuid(_):
            used_arguments = register_mock.call_args[0]
            self.assertIsNotNone(used_arguments)
            soledad_invalid_auth_event = used_arguments[0]
            self.assertEqual(soledad_invalid_auth_event, events.SOLEDAD_INVALID_AUTH_TOKEN)
            used_log_out_method = used_arguments[1]
            used_log_out_method(events.SOLEDAD_INVALID_AUTH_TOKEN, {'uuid': 'some_uuid'})
            mock_service_log_user_out.assert_called_once_with(user_id='some_uuid')

        def _assert_user_logged_out_using_email_id(_):
            mock_service_log_user_out.reset_mock()
            used_arguments = register_mock.call_args[0]
            used_log_out_method = used_arguments[1]
            used_log_out_method(events.SOLEDAD_INVALID_AUTH_TOKEN, 'haha@ayo.yo')
            mock_service_log_user_out.assert_called_once_with(user_id='haha@ayo.yo', using_email=True)

        d.addCallback(_assert_user_logged_out_using_uuid)
        d.addCallback(_assert_user_logged_out_using_email_id)
        return d
