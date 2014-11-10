import unittest
from mock import patch, MagicMock, ANY

from pixelated.config.app_factory import create_app


class AppFactoryTest(unittest.TestCase):

    @patch('pixelated.config.app_factory.reactor')
    def test_that_create_app_binds_to_port(self, reactor_mock):
        app_mock = MagicMock()

        create_app(app_mock, '127.0.0.1', 12345)

        reactor_mock.listenTCP.assert_called_once_with(12345, ANY, interface='127.0.0.1')
