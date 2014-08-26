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
import json


class Tag:

    LEAP_FLAGS_TAGS = {
        '\\Deleted': 'trash',
        '\\Draft': 'drafts',
        '\\Recent': 'inbox'
    }

    @classmethod
    def from_flags(cls, flags):
        return set(filter(None, (cls.from_flag(flag) for flag in flags)))

    @classmethod
    def from_flag(cls, flag):
        if flag in cls.LEAP_FLAGS_TAGS.keys():
            return Tag(cls.LEAP_FLAGS_TAGS[flag])
        if flag.startswith('tag_'):
            return Tag(cls._remove_prefix(flag))
        return None

    @classmethod
    def _remove_prefix(cls, flag_name):
        return flag_name.replace('tag_', '', 1)

    def __init__(self, name, default=False):
        self.name = name
        self.default = default
        self.ident = name.__hash__()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()

    def as_dict(self):
        return {
            'name': self.name,
            'default': self.default,
            'ident': self.ident,
            'counts': {
                'total': 0,
                'read': 0,
                'starred': 0,
                'replied': 0
            }
        }

    def __repr__(self):
        return self.name
