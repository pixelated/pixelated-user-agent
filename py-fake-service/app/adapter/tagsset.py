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
from tag import Tag


class TagsSet:

    def __init__(self):
        self.tags = {}
        self.ident = 0

    def add(self, mbox_mail):
        tags = mbox_mail.get('X-TW-Pixelated-Tags').split(', ')
        for tag in tags:
            tag = self._create_new_tag(tag)
            tag.increment_count()

    def all_tags(self):
        return self.tags.values()

    def mark_as_read(self, tags):
        for tag in tags:
            tag = tag.lower()
            tag = self.tags.get(tag)
            tag.increment_read()

    def increment_tag_total_count(self, tagname):
        tag = self.tags.get(tagname)
        if tag:
            tag.increment_count()
        else:
            self._create_new_tag(tagname)

    def decrement_tag_total_count(self, tag):
        self.tags.get(tag).decrement_count()

    def _create_new_tag(self, tag):
        tag = Tag(tag, self.ident)
        tag = self.tags.setdefault(tag.name, tag)
        self.ident += 1
        return tag
