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
from pixelated.controllers import SyncInfoController
from mockito import *
import json


class SyncInfoControllerTest(unittest.TestCase):

    def setUp(self):
        self.controller = SyncInfoController()

    def _set_count(self, current, total):
        soledad_sync_data = mock()
        soledad_sync_data.content = "%s/%s" % (current, total)
        self.controller.set_sync_info(soledad_sync_data)

    def get_sync_info(self):
        return json.loads(self.controller.sync_info().data)

    def test_is_not_syncing_if_total_is_equal_to_current(self):
        self._set_count(total=0, current=0)

        sync_info = self.get_sync_info()

        self.assertFalse(sync_info['is_syncing'])

    def test_is_syncing_if_total_is_not_equal_to_current_and_adds_count(self):
        self._set_count(total=10, current=5)

        sync_info = self.get_sync_info()

        self.assertTrue(sync_info['is_syncing'])
        self.assertEquals(5, sync_info['count']['current'])
        self.assertEquals(10, sync_info['count']['total'])
        self.assertEquals(0.5, sync_info['count']['progress'])
