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
from pixelated.adapter.pixelated_mail import PixelatedMail

from pixelated.adapter.pixelated_mailbox import PixelatedMailbox
from pixelated.adapter.pixelated_mailboxes import PixelatedMailBoxes
from mockito import *


class PixelatedMailboxesTest(unittest.TestCase):
    def setUp(self):
        self.account = mock()
        self.drafts_mailbox = mock()
        self.drafts_mailbox.mailbox_name = 'drafts'
        self.mailboxes = PixelatedMailBoxes(self.account)
        self.mailboxes.drafts = lambda: self.drafts_mailbox

    def test_search_for_tags(self):
        mailbox = mock()
        self.account.mailboxes = ['INBOX']
        tags_to_search_for = {'tags': ['inbox', 'custom_tag']}

        when(PixelatedMailbox).create(self.account, 'INBOX').thenReturn(mailbox)
        when(mailbox).mails_by_tags(any(list)).thenReturn(["mail"])

        mails = self.mailboxes.mails_by_tag(tags_to_search_for['tags'])

        self.assertEqual(1, len(mails))
        self.assertEqual("mail", mails[0])

    def test_add_draft(self):
        mail = PixelatedMail()
        when(self.drafts_mailbox).add(mail).thenReturn(1)

        self.mailboxes.add_draft(mail)

        verify(self.drafts_mailbox).add(mail)
        self.assertEqual('drafts', mail.mailbox_name)
        self.assertEqual(1, mail.uid)

    def test_update_draft(self):
        mail = PixelatedMail()
        when(self.drafts_mailbox).add(mail).thenReturn(1)

        self.mailboxes.update_draft(mail)

        inorder.verify(self.drafts_mailbox).add(mail)
        inorder.verify(self.drafts_mailbox).remove(mail)

        self.assertEqual('drafts', mail.mailbox_name)
        self.assertEqual(1, mail.uid)
