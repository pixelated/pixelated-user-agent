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


class Tags:

    SPECIAL_TAGS = ['inbox', 'sent', 'drafts', 'trash']

    def __init__(self):
        self.tags = {}
        self.create_default_tags()

    def create_default_tags(self):
        for name in self.SPECIAL_TAGS:
            self.tags[name] = self.add(name)

    def add(self, tag_input):
        if tag_input.__class__.__name__ == 'Tag':
            tag_input = tag_input.name
        tag = Tag(tag_input, tag_input in self.SPECIAL_TAGS)
        self.tags[tag_input] = tag
        return tag

    def find(self, name):
        return self.tags[name]

    def __len__(self):
        return len(self.tags)

    def __iter__(self):
        return self.tags.itervalues()

    def as_dict(self):
        return [tag.as_dict() for tag in self.tags.values()]
