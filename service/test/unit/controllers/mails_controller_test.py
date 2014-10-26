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
        self.mail_service = mock()
        self.search_engine = mock()
        draft_service = mock()

        self.mails_controller = MailsController(mail_service=self.mail_service,
                                                draft_service=draft_service,
                                                search_engine=self.search_engine)

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

    def test_fetching_mail_gets_mail_from_mail_service(self):
        mail = mock()
        mail.as_dict = lambda: {'ident': 1, 'body': 'le mail body'}
        when(self.mail_service).mail(1).thenReturn(mail)

        response = self.mails_controller.mail(1)

        verify(self.mail_service).mail(1)
        self.assertEqual(response.data, '{"body": "le mail body", "ident": 1}')

    def test_marking_mail_as_read_set_mail_as_read_on_the_service(self):
        mail = mock()
        when(self.mail_service).mark_as_read(1).thenReturn(mail)
        when(self.search_engine).index_mail(mail).thenReturn(None)

        self.mails_controller.mark_mail_as_read(1)

        verify(self.mail_service).mark_as_read(1)
        verify(self.search_engine).index_mail(mail)

    def test_marking_mail_as_unread_set_mail_as_unread_on_the_service(self):
        mail = mock()
        when(self.mail_service).mark_as_unread(1).thenReturn(mail)
        when(self.search_engine).index_mail(mail).thenReturn(None)

        self.mails_controller.mark_mail_as_unread(1)

        verify(self.mail_service).mark_as_unread(1)
        verify(self.search_engine).index_mail(mail)

    def test_delete_permanently_when_mail_in_trash(self):
        mail = mock()
        mail.mailbox_name ='TRASH'
        when(self.mail_service).mail(1).thenReturn(mail)
        self.mails_controller.delete_mail(1)

        verify(self.mail_service).delete_permanent(1)

    def test_move_message_to_trash(self):
        mail = mock()
        mail.mailbox_name ='INBOX'
        when(self.mail_service).mail(1).thenReturn(mail)
        when(self.mails_controller).delete_mail(1).thenReturn(mail)
        when(self.search_engine).index_mail(mail)

        verify(self.search_engine).index_mail(mail)

    def _successfuly_send_mail(self, ident, mail):
        sent_mail = mock()
        mail.mailbox_name ='TRASH'
        sent_mail.as_dict = lambda: self.input_mail.json

        return sent_mail

    def _send_that_throws_exception(self, ident, mail):
        raise Exception('email sending failed', 'more information of error', 123, 'there was a code before this')




    

