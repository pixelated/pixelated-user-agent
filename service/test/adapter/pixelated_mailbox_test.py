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
import test_helper
from mockito import *


class PixelatedMailboxTest(unittest.TestCase):
    def setUp(self):
        self.tag_service = mock()
        self.querier = mock()
        self.mailbox = PixelatedMailbox('INBOX', self.querier, tag_service=self.tag_service)

    def test_mailbox_tag_is_added_when_recent_mail_arrives(self):
        recent_leap_mail = test_helper.leap_mail(uid=0, mbox='INBOX', flags=['\\Recent'])
        when(self.querier).all_mails_by_mailbox('INBOX').thenReturn([PixelatedMail.from_soledad(*recent_leap_mail, soledad_querier=self.querier)])

        self.assertIn('inbox', self.mailbox.mails()[0].tags)

    def test_mailbox_tag_is_ignored_for_non_recent_mail(self):
        recent_leap_mail = test_helper.leap_mail(uid=0, mbox='INBOX', flags=[])
        when(self.querier).all_mails_by_mailbox('INBOX').thenReturn([PixelatedMail.from_soledad(*recent_leap_mail, soledad_querier=self.querier)])

        self.assertNotIn('spam', self.mailbox.mails()[0].tags)

    def test_remove_message_from_mailbox(self):
        mail = PixelatedMail()
        when(self.querier).mail(1).thenReturn(mail)

        self.mailbox.remove(1)

        verify(self.querier).remove_mail(mail)
