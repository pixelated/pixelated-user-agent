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
from twisted.trial import unittest
from test.support.integration.app_test_client import AppTestClient


class SoledadTestBase(unittest.TestCase, AppTestClient):
    # these are so long because our CI is so slow at the moment.
    DEFERRED_TIMEOUT = 120
    DEFERRED_TIMEOUT_LONG = 300

    def setUp(self):
        return self.start_client()

    def tearDown(self):
        self.cleanup()
