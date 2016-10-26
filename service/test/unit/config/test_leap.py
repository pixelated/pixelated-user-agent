from leap.soledad.common.errors import InvalidAuthTokenError
from mock import MagicMock, patch, Mock
from twisted.trial import unittest
from twisted.internet import defer
from pixelated.config.leap import create_leap_session, BootstrapUserServices
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


class TestUserBootstrap(unittest.TestCase):

    def setUp(self):
        self._service_factory = Mock()
        self._provider = Mock()
        self._user_bootstrap = BootstrapUserServices(self._service_factory, self._provider)

        username = 'ayoyo'
        password = 'ayoyo_password'
        self.username = username
        self.password = password

        user_auth = Mock()
        user_auth.username = username
        self.uuid = 'some_user_uuid'
        user_auth.uuid = self.uuid
        self.user_auth = user_auth

        leap_session = Mock()
        leap_session.user_auth = user_auth
        leap_session.fresh_account = False
        self.leap_session = leap_session

    @patch('pixelated.config.leap.create_leap_session')
    def test_should_create_leap_session(self, mock_create_leap_session):
        mock_create_leap_session.return_value = self.leap_session
        self._service_factory.has_session.return_value = False

        self._user_bootstrap.setup(self.user_auth, self.password)

        mock_create_leap_session.called_once_with(self._provider, self.username, self.password, self.user_auth)

    @patch('pixelated.config.leap.create_leap_session')
    def test_should_setup_user_services_and_map_email(self, mock_create_leap_session):
        mock_create_leap_session.return_value = self.leap_session
        self._service_factory.has_session.return_value = False

        self._user_bootstrap.setup(self.user_auth, self.password)

        self._service_factory.create_services_from.assert_called_once_with(self.leap_session)
        self._service_factory.map_email.assert_called_once_with(self.username, self.uuid)

    @patch('pixelated.config.leap.create_leap_session')
    def test_should_not_user_services_if_there_is_already_a_session(self, mock_create_leap_session):
        mock_create_leap_session.return_value = self.leap_session
        self._service_factory.has_session.return_value = True

        self._user_bootstrap.setup(self.user_auth, self.password)

        self.assertFalse(self._service_factory.create_services_from.called)

    @patch('pixelated.config.leap.add_welcome_mail')
    @patch('pixelated.config.leap.create_leap_session')
    def test_should_add_welcome_email_on_a_fresh_account(self, mock_create_leap_session, mock_add_welcome_email):
        self.leap_session.fresh_account = True
        mail_store = Mock()
        self.leap_session.mail_store = mail_store
        mock_create_leap_session.return_value = self.leap_session
        self._service_factory.has_session.return_value = False
        some_language = 'en-US'

        self._user_bootstrap.setup(self.user_auth, self.password, '')

        mock_add_welcome_email.called_once_with(mail_store, some_language)
