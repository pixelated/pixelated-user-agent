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


class Tag:
    DEFAULT_TAGS = ["inbox", "sent", "trash", "drafts"]

    def __init__(self, name, ident):
        self.counts = {
            'total': 0,
            'read': 0,
            'starred': 0,
            'reply': 0
        }

        self.ident = ident
        self.name = name.lower()
        self.default = name in self.DEFAULT_TAGS

    def increment_count(self):
        self.counts['total'] += 1

    def increment_read(self):
        self.counts['read'] += 1

    def decrement_count(self):
        self.counts['total'] -= 1
