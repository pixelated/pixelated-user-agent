#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from mock import patch

from pixelated.bitmask_libraries.session import LeapSession
from abstract_leap_test import AbstractLeapTest


class SessionTest(AbstractLeapTest):
    def test_background_jobs_are_started(self):
        self.config.start_background_jobs = True

        with patch('pixelated.bitmask_libraries.session.reactor.callFromThread', new=_execute_func) as _:
            self._create_session()

            self.mail_fetcher_mock.start_loop.assert_called_once_with()

    def test_background_jobs_are_not_started(self):
        self.config.start_background_jobs = False

        with patch('pixelated.bitmask_libraries.session.reactor.callFromThread', new=_execute_func) as _:
            self._create_session()

            self.assertFalse(self.mail_fetcher_mock.start_loop.called)

    def test_that_close_stops_background_jobs(self):
        with patch('pixelated.bitmask_libraries.session.reactor.callFromThread', new=_execute_func) as _:
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
