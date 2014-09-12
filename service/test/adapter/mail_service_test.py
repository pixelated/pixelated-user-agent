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

    def test_send_mail(self):
        mail = "mail"

        self.mail_service.send(mail)

        verify(self.mail_sender).sendmail(mail)

    def test_mark_as_read(self):
        mail = mock()
        when(self.mail_service).mail(any()).thenReturn(mail)
        self.mail_service.mark_as_read(1)

        verify(mail).mark_as_read()

    def test_create_draft(self):
        mail = ''

        self.mail_service.create_draft(mail)

        verify(self.mailboxes).add_draft(mail)
