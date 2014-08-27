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

import test_helper
from pixelated.adapter.tag import Tag
from pixelated.adapter.pixelated_mailbox import PixelatedMailbox


class TestPixelatedMailbox(unittest.TestCase):

    def test_retrieve_all_tags_from_mailbox(self):
        leap_flags = ['\\Deleted', '\\Draft', '\\Recent', 'tag_custom', 'should_ignore_all_from_here', 'List']
        mailbox = PixelatedMailbox(test_helper.leap_mailbox(leap_flags=leap_flags))

        self.assertEquals(set([Tag('trash'), Tag('inbox'), Tag('drafts'), Tag('custom')]), mailbox.all_tags())

    def test_new_tags_are_added_to_mailbox(self):
        leap_flags = ['\\Deleted', 'tag_custom_one', 'tag_custom_two']
        leap_mailbox_mock = test_helper.leap_mailbox(leap_flags=leap_flags)
        mailbox = PixelatedMailbox(leap_mailbox_mock)
        tags = [Tag('custom_one'), Tag('custom_three')]
        mailbox.update_tags(tags)

        expected = set(('\\Deleted', 'tag_custom_one', 'tag_custom_two', 'tag_custom_three'))
        actual_args = set(leap_mailbox_mock.setFlags.call_args[0][0])

        self.assertEquals(expected, actual_args)
