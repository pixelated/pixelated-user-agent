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

from pixelated.adapter.pixelated_mailbox import PixelatedMailbox
from pixelated.adapter.pixelated_mailboxes import PixelatedMailBoxes
from mockito import *


class PixelatedMailboxesTest(unittest.TestCase):
    def setUp(self):
        self.account = mock()
        self.mailboxes = PixelatedMailBoxes(self.account)

    def test_search_for_tags(self):
        # given
        mailbox = mock()
        self.account.mailboxes = ['INBOX']
        tags_to_search_for = {'tags': ['inbox', 'custom_tag']}

        when(PixelatedMailbox).create(self.account, 'INBOX').thenReturn(mailbox)
        when(mailbox).mails_by_tags(any(list)).thenReturn(["mail"])

        # when
        mails = self.mailboxes.mails_by_tag(tags_to_search_for['tags'])

        # then
        self.assertEqual(1, len(mails))
        self.assertEqual("mail", mails[0])

