from leap.soledad.common.errors import InvalidAuthTokenError
from mock import MagicMock, patch
from twisted.trial import unittest
from twisted.internet import defer
from pixelated.config.leap import authenticate_user


class TestAuth(unittest.TestCase):

    @patch('pixelated.config.leap.LeapSessionFactory')
    @defer.inlineCallbacks
    def test_authenticate_user_calls_initinal_sync(self, session_factory__ctor_mock):
        session_factory_mock = session_factory__ctor_mock.return_value
        provider_mock = MagicMock()
        auth_mock = MagicMock()
        session = MagicMock()

        session_factory_mock.create.return_value = session

        yield authenticate_user(provider_mock, 'username', 'password', auth=auth_mock)

        session.initial_sync.assert_called_with()

    @patch('pixelated.config.leap.LeapSessionFactory')
    @defer.inlineCallbacks
    def test_authenticate_user_calls_initial_sync_a_second_time_if_invalid_auth_exception_is_raised(self, session_factory__ctor_mock):
        session_factory_mock = session_factory__ctor_mock.return_value
        provider_mock = MagicMock()
        auth_mock = MagicMock()
        session = MagicMock()

        session.initial_sync.side_effect = [InvalidAuthTokenError, defer.succeed(None)]
        session_factory_mock.create.return_value = session

        yield authenticate_user(provider_mock, 'username', 'password', auth=auth_mock)

        session.close.assert_called_with()
        self.assertEqual(2, session.initial_sync.call_count)
