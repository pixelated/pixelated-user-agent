from leap.soledad.common.errors import InvalidAuthTokenError
from mock import MagicMock, patch
from twisted.trial import unittest
from twisted.internet import defer
from pixelated.config.leap import create_leap_session
from pixelated.config.sessions import LeapSessionFactory, SessionCache


class TestAuth(unittest.TestCase):

    @patch('pixelated.config.sessions.SessionCache.session_key')
    @defer.inlineCallbacks
    def test_create_leap_session_calls_initial_sync_and_caches_sessions(self, mock_session_key):
        mock_session_key.return_value = 'mocked key'
        provider_mock = MagicMock()
        auth_mock = MagicMock()
        session = MagicMock()
        with patch.object(LeapSessionFactory, '_create_new_session', return_value=session):
            yield create_leap_session(provider_mock, 'username', 'password', auth=auth_mock)

        session.first_required_sync.assert_called_with()
        self.assertEqual({'mocked key': session}, SessionCache.sessions)

    @patch('pixelated.config.sessions.SessionCache.lookup_session')
    @defer.inlineCallbacks
    def test_create_leap_session_uses_caches_when_available_and_not_sync(self, mock_cache_lookup_session):
        mock_cache_lookup_session.return_value = 'mocked key'
        provider_mock = MagicMock()
        auth_mock = MagicMock()
        session = MagicMock()
        mock_cache_lookup_session.return_value = session

        with patch.object(LeapSessionFactory, '_create_new_session', return_value=session):
            returned_session = yield create_leap_session(provider_mock, 'username', 'password', auth=auth_mock)

        self.assertFalse(session.first_required_sync.called)
        self.assertEqual(session, returned_session)
