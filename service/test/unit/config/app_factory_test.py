import unittest

from mock import patch, MagicMock, ANY
import pixelated
from pixelated.config.app_factory import create_app


class AppFactoryTest(unittest.TestCase):

    class MockConfig:
        def __init__(self, port, host, sslkey=None, sslcert=None):
            self.port = port
            self.host = host
            self.sslkey = sslkey
            self.sslcert = sslcert

    @patch('pixelated.config.app_factory.reactor')
    def test_that_create_app_binds_to_tcp_port_if_no_ssl_options(self, reactor_mock):
        app_mock = MagicMock()

        create_app(app_mock, AppFactoryTest.MockConfig(12345, '127.0.0.1'))

        reactor_mock.listenTCP.assert_called_once_with(12345, ANY, interface='127.0.0.1')

    @patch('pixelated.config.app_factory.reactor')
    def test_that_create_app_binds_to_ssl_if_ssl_options(self, reactor_mock):
        app_mock = MagicMock()
        pixelated.config.app_factory._ssl_options = lambda _: 'options'

        create_app(app_mock, AppFactoryTest.MockConfig(12345, '127.0.0.1', sslkey="sslkey", sslcert="sslcert"))

        reactor_mock.listenSSL.assert_called_once_with(12345, ANY, 'options', interface='127.0.0.1')
