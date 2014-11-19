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

from test.support.integration import *
from pixelated.adapter.status import Status


class MarkAsReadUnreadTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    def tearDown(self):
        SoledadTestBase.tearDown(self)

    def test_mark_single_as_read(self):
        input_mail = MailBuilder().build_input_mail()
        self.client.add_mail_to_inbox(input_mail)

        mails = self.get_mails_by_tag('inbox')
        self.assertNotIn('read', mails[0].status)

        self.mark_as_read(input_mail.ident)

        mails = self.get_mails_by_tag('inbox')
        self.assertIn('read', mails[0].status)

    def test_mark_single_as_unread(self):
        input_mail = MailBuilder().with_status([Status.SEEN]).build_input_mail()
        self.client.add_mail_to_inbox(input_mail)

        self.mark_as_unread(input_mail.ident)
        mail = self.get_mails_by_tag('inbox')[0]

        self.assertNotIn('read', mail.status)

    def test_mark_many_mails_as_unread(self):
        input_mail = MailBuilder().with_status([Status.SEEN]).build_input_mail()
        input_mail2 = MailBuilder().with_status([Status.SEEN]).build_input_mail()

        self.client.add_mail_to_inbox(input_mail)
        self.client.add_mail_to_inbox(input_mail2)

        self.mark_many_as_unread([input_mail.ident, input_mail2.ident])

        mails = self.get_mails_by_tag('inbox')

        self.assertNotIn('read', mails[0].status)
        self.assertNotIn('read', mails[1].status)

    def test_mark_many_mails_as_read(self):
        input_mail = MailBuilder().build_input_mail()
        input_mail2 = MailBuilder().build_input_mail()

        self.client.add_mail_to_inbox(input_mail)
        self.client.add_mail_to_inbox(input_mail2)

        mails = self.get_mails_by_tag('inbox')

        self.assertNotIn('read', mails[0].status)
        self.assertNotIn('read', mails[1].status)

        response = self.mark_many_as_read([input_mail.ident, input_mail2.ident])
        self.assertEquals(200, response.code)

        mails = self.get_mails_by_tag('inbox')

        self.assertIn('read', mails[0].status)
        self.assertIn('read', mails[1].status)

    def test_mark_mixed_status_as_read(self):
        input_mail = MailBuilder().build_input_mail()
        input_mail2 = MailBuilder().with_status([Status.SEEN]).build_input_mail()

        self.client.add_mail_to_inbox(input_mail)
        self.client.add_mail_to_inbox(input_mail2)

        mails = self.get_mails_by_tag('inbox')

        read_mails = filter(lambda x: 'read' in x.status, mails)
        unread_mails = filter(lambda x: 'read' not in x.status, mails)
        self.assertEquals(1, len(unread_mails))
        self.assertEquals(1, len(read_mails))

        response = self.mark_many_as_read([input_mail.ident, input_mail2.ident])
        self.assertEquals(200, response.code)

        mails = self.get_mails_by_tag('inbox')

        self.assertIn('read', mails[0].status)
        self.assertIn('read', mails[1].status)
