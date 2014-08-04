from mock import patch

from app.bitmask_libraries.session import LeapSession
from abstract_leap_test import AbstractLeapTest


class SessionTest(AbstractLeapTest):
    def test_background_jobs_are_started(self):
        self.config.start_background_jobs = True

        with patch('app.bitmask_libraries.session.reactor.callFromThread', new=_execute_func) as _:
            self._create_session()

            self.mail_fetcher_mock.start_loop.assert_called_once_with()

    def test_background_jobs_are_not_started(self):
        self.config.start_background_jobs = False

        with patch('app.bitmask_libraries.session.reactor.callFromThread', new=_execute_func) as _:
            self._create_session()

            self.assertFalse(self.mail_fetcher_mock.start_loop.called)

    def test_that_close_stops_background_jobs(self):
        with patch('app.bitmask_libraries.session.reactor.callFromThread', new=_execute_func) as _:
            session = self._create_session()

            session.close()

            self.mail_fetcher_mock.stop.assert_called_once_with()

    def test_that_sync_deferes_to_soledad(self):
        session = self._create_session()

        session.sync()

        self.soledad_session.sync.assert_called_once_with()

    def test_account_email(self):
        session = self._create_session()
        self.assertEqual('test_user@some-server.test', session.account_email())

    def _create_session(self):
        return LeapSession(self.provider, self.srp_session, self.soledad_session, self.nicknym, self.soledad_account,
                           self.mail_fetcher_mock)


def _execute_func(func):
    func()
