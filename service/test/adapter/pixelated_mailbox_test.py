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
import os

import test_helper
from pixelated.adapter.tag import Tag
from pixelated.adapter.tag_index import TagIndex
from pixelated.adapter.pixelated_mailbox import PixelatedMailbox


class TestPixelatedMailbox(unittest.TestCase):

    def setUp(self):
        self.db_file_path = '/tmp/test_tags'

    def tearDown(self):
        os.remove(self.db_file_path + '.db')

    def test_special_tags_always_exists(self):
        mailbox = PixelatedMailbox(test_helper.leap_mailbox(), self.db_file_path)
        self.assertEquals(mailbox.SPECIAL_TAGS, mailbox.all_tags())

    def test_retrieve_all_tags_from_mailbox(self):
        tag_index = TagIndex(self.db_file_path)
        tag_index.set(Tag('one_tag'))
        tag_index.set(Tag('two_tag'))
        tag_index.close_db()
        mailbox = PixelatedMailbox(test_helper.leap_mailbox(), self.db_file_path)
        expected_tags = set([Tag('one_tag'), Tag('two_tag')]).union(mailbox.SPECIAL_TAGS)
        self.assertEquals(expected_tags, mailbox.all_tags())

    def test_notify_tags_updated_method_properly_changes_tags_state(self):
        tag_index = TagIndex(self.db_file_path)
        tag = Tag('one_tag')
        tag.increment(12)
        tag_index.set(tag)
        tag_index.close_db()
        mailbox = PixelatedMailbox(test_helper.leap_mailbox(), self.db_file_path)
        self.assertEquals(0, mailbox.tag_index.get('inbox').total)
        mailbox.notify_tags_updated(set(['inbox']), set(['one_tag']), 12)
        self.assertEquals(1, mailbox.tag_index.get('inbox').total)
