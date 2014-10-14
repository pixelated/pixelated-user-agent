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
from mockito import *
from pixelated.controllers.mails_controller import MailsController

class TestMailsController(unittest.TestCase):

    def setUp(self):
        self.mail_service = mock() #MailService(pixelated_mailboxes, pixelated_mail_sender, tag_service, soledad_querier)
        search_engine = mock() #SearchEngine()
        draft_service = mock() #DraftService(pixelated_mailboxes)

        self.mails_controller = MailsController(mail_service=self.mail_service,
                                           draft_service=draft_service,
                                           search_engine=search_engine)

        self.input_mail = mock()
        self.input_mail.json = {'header': {'from': 'a@a.a', 'to': 'b@b.b'},
                                'ident': 1,
                                'tags': [],
                                'status': [],
                                'security_casing': {},
                                'body': 'email body'}
    def tearDown(self):
        unstub()

    def test_sending_mail_return_sent_mail_data_when_send_succeeds(self):
        self.mail_service.send = self._successfuly_send_mail

        result = self.mails_controller.send_mail(self.input_mail)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, '{"status": [], "body": "email body", "ident": 1, "tags": [], "header": {"to": "b@b.b", "from": "a@a.a"}, "security_casing": {}}')

    def test_sending_mail_return_error_message_when_send_fails(self):
        self.mail_service.send = self._send_that_throws_exception

        result = self.mails_controller.send_mail(self.input_mail)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(result.data, '{"message": "email sending failed\\nmore information of error\\n123\\nthere was a code before this"}')

    def _successfuly_send_mail(self, ident, mail):
        sent_mail = mock()
        sent_mail.as_dict = lambda: self.input_mail.json

        return sent_mail

    def _send_that_throws_exception(self, ident, mail):
        raise Exception('email sending failed', 'more information of error', 123, 'there was a code before this')

