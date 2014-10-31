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
from pixelated.controllers import respond_json


class SyncInfoController:
    def __init__(self):
        self.current = 0
        self.total = 0

    def _get_progress(self):
        if self.total == 0:
            return 0
        return self.current / float(self.total)

    def set_sync_info(self, soledad_sync_status):
        self.current, self.total = map(int, soledad_sync_status.content.split('/'))

    def sync_info(self, request):
        _sync_info = {
            'is_syncing': self.current != self.total,
            'count': {
                'current': self.current,
                'total': self.total,
                'progress': self._get_progress()
            }
        }
        return respond_json(_sync_info, request)
