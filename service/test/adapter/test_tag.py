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

from pixelated.adapter.tag import Tag
import test_helper


class TestTag(unittest.TestCase):

    def test_leap_recent_flag_is_translated_to_inbox_tag(self):
        tag = Tag.from_flag('\\Recent')
        self.assertEquals(Tag('inbox'), tag)

    def test_leap_deleted_flag_is_translated_to_trash_tag(self):
        tag = Tag.from_flag('\\Deleted')
        self.assertEquals(Tag('trash'), tag)

    def test_leap_draft_flag_is_translated_to_draft_tag(self):
        tag = Tag.from_flag('\\Draft')
        self.assertEquals(Tag('drafts'), tag)

    def test_leap_flags_that_are_custom_tags_are_handled(self):
        tag = Tag.from_flag('tag_work')
        self.assertEquals(Tag('work'), tag)

    def test_custom_tags_containing_our_prefix_are_handled(self):
        tag = Tag.from_flag('tag_tag_work_tag_')
        self.assertEquals(Tag('tag_work_tag_'), tag)

    def test_bulk_conversion(self):
        tags = Tag.from_flags(['\\Answered', '\\Seen', '\\Recent', 'tag_a_custom', 'List'])
        self.assertEquals(set([Tag('inbox'), Tag('a_custom')]), tags)
