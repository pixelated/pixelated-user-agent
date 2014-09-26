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
from pixelated.adapter.pixelated_mail import InputMail
from mockito import *
import test.adapter.test_helper as test_helper
import json
import pixelated.adapter.pixelated_mail


class UserAgentTest(unittest.TestCase):

    def setUp(self):
        self.app = pixelated.user_agent.app.test_client()
        self.mail_service = mock()

        pixelated.user_agent.DISABLED_FEATURES = []
        pixelated.user_agent.mail_service = self.mail_service
        self.input_mail = None
        pixelated.adapter.pixelated_mail.input_mail_from_dict = lambda x: self.input_mail

    def test_create_or_send_draft_should_create_draft_if_mail_has_no_ident(self):
        self.input_mail = self.draft()

        self.app.post('/mails', data='{}', content_type="application/json")

        verify(self.mail_service).create_draft(self.input_mail)

    def test_create_or_send_draft_should_send_draft_if_mail_has_ident(self):
        self.input_mail = self.draft()

        self.app.post('/mails', data='{"ident":1}', content_type="application/json")

        verify(self.mail_service).send_draft(self.input_mail)

    def test_update_draft(self):
        self.input_mail = self.draft()

        when(self.mail_service).update_draft(1, self.input_mail).thenReturn(self.input_mail)

        self.app.put('/mails', data='{"ident":1}', content_type="application/json")

        verify(self.mail_service).update_draft(1, self.input_mail)



    def draft(self):
        return test_helper.input_mail()
