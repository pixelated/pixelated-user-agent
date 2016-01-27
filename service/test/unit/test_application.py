import unittest

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
