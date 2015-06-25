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

    @patch('pixelated.application.reactor')
    @patch('pixelated.application.Services')
    def test_that_create_app_binds_to_tcp_port_if_no_ssl_options(self, services_mock, reactor_mock):
        app_mock = MagicMock()
        leap_session = MagicMock()
        config = ApplicationTest.MockConfig(12345, '127.0.0.1', leap_session)

        d = pixelated.application.start_user_agent(app_mock, config.host, config.port, config.sslkey, config.sslcert, config.home, leap_session)

        def _assert(_):
            services_mock.assert_called_once_with(config.home, leap_session)

            reactor_mock.listenTCP.assert_called_once_with(12345, ANY, interface='127.0.0.1')
            app_mock.stopListening.assert_called()

        d.addCallback(_assert)
        return d

    @patch('pixelated.application.reactor')
    @patch('pixelated.application.Services')
    def test_that_create_app_binds_to_ssl_if_ssl_options(self, services_mock, reactor_mock):
        app_mock = MagicMock()
        leap_session = MagicMock()
        pixelated.application._ssl_options = lambda x, y: 'options'

        config = ApplicationTest.MockConfig(12345, '127.0.0.1', sslkey="sslkey", sslcert="sslcert")

        d = pixelated.application.start_user_agent(app_mock, config.host, config.port, config.sslkey, config.sslcert, config.home, leap_session)

        def _assert(_):
            services_mock.assert_called_once_with(config.home, leap_session)

            reactor_mock.listenSSL.assert_called_once_with(12345, ANY, 'options', interface='127.0.0.1')
            app_mock.stopListening.assert_called()

        d.addCallback(_assert)
        return d
