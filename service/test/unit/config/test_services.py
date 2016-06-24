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
import unittest

from mockito import mock, verify

from pixelated.config.services import Services, ServicesFactory


class ServicesTest(unittest.TestCase):

    def setUp(self):
        super(ServicesTest, self).setUp()
        self.leap_session = mock()
        config = mock()
        self.leap_session.config = config
        self.services = Services(self.leap_session)

    def test_close_services_closes_the_underlying_leap_session(self):
        self.services.close()
        verify(self.leap_session).close()


class ServicesFactoryTest(unittest.TestCase):

    def test_online_sessions_counts_logged_in_users(self):
        service_factory = ServicesFactory(mock())
        service_factory.add_session('some_id1', mock())
        service_factory.add_session('some_id2', mock())

        self.assertEqual(2, service_factory.online_sessions())
