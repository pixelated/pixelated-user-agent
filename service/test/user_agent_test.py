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
import pixelated.user_agent
from pixelated.adapter.pixelated_mail import PixelatedMail
from mockito import *
import pixelated.adapter.pixelated_mail


class UserAgentTest(unittest.TestCase):

    def setUp(self):
        self.app = pixelated.user_agent.app.test_client()
        self.mail_service = mock()

        pixelated.user_agent.DISABLED_FEATURES = []
        pixelated.user_agent.mail_service = self.mail_service

    def test_create_or_send_draft_should_create_draft_if_mail_has_no_ident(self):
        mail = self.mail_without_ident()
        pixelated.adapter.pixelated_mail.from_dict = lambda self: mail  # has no ident

        self.app.post('/mails', data='{}', content_type="application/json")

        verify(self.mail_service).create_draft(mail)

    def test_create_or_send_draft_should_send_draft_if_mail_has_ident(self):
        mail = self.mail_with_ident()
        pixelated.adapter.pixelated_mail.from_dict = lambda self: mail  # does have ident

        self.app.post('/mails', data='{}', content_type="application/json")

        verify(self.mail_service).send_draft(mail)

    def mail_without_ident(self):
        mail = PixelatedMail()
        mail.ident = ''
        return mail

    def mail_with_ident(self):
        mail = PixelatedMail()
        mail.ident = 1
        return mail
