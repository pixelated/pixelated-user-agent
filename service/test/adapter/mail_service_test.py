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

from pixelated.adapter.mail_service import MailService
from mockito import *


class TestMailService(unittest.TestCase):
    def setUp(self):
        self.mailboxes = mock()
        self.mail_sender = mock()
        self.mail_service = MailService(self.mailboxes, self.mail_sender)

    def test_search_without_query_returns_unfiltered_mailbox(self):
        mailbox_inbox = mock()
        when(mailbox_inbox).mails().thenReturn(["mail"])
        when(self.mailboxes).inbox().thenReturn(mailbox_inbox)

        mails = self.mail_service.mails({})

        self.assertEqual(1, len(mails))

    def test_send_mail(self):
        mail = "mail"

        self.mail_service.send(mail)

        verify(self.mail_sender).sendmail(mail)
