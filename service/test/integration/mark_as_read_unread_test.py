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

from test.support.integration_helper import MailBuilder, SoledadTestBase


class MarkAsReadUnreadTest(unittest.TestCase, SoledadTestBase):

    def setUp(self):
        self.setup_soledad()

    def tearDown(self):
        self.teardown_soledad()

    def test_mark_single_as_read(self):
        input_mail = MailBuilder().build_input_mail()
        self.add_mail_to_inbox(input_mail)

        mails = self.get_mails_by_tag('inbox')
        self.assertNotIn('read', mails[0].status)

        self.mark_as_read(input_mail.ident)

        mails = self.get_mails_by_tag('inbox')
        self.assertIn('read', mails[0].status)

    def test_mark_single_as_unread(self):
        input_mail = MailBuilder().with_status('read').build_input_mail()

        self.add_mail_to_inbox(input_mail)

        self.mark_as_unread(input_mail.ident)

        mails = self.get_mails_by_tag('inbox')
        self.assertNotIn('read', mails[0].status)

    def test_mark_many_mails_as_unread(self):
        input_mail = MailBuilder().with_status('read').build_input_mail()
        input_mail2 = MailBuilder().with_status('read').build_input_mail()

        self.add_mail_to_inbox(input_mail)
        self.add_mail_to_inbox(input_mail2)

        self.mark_many_as_unread([input_mail.ident, input_mail2.ident])

        mails = self.get_mails_by_tag('inbox')

        self.assertNotIn('read', mails[0].status)
        self.assertNotIn('read', mails[1].status)

    def test_mark_many_mails_as_read(self):
        input_mail = MailBuilder().build_input_mail()
        input_mail2 = MailBuilder().build_input_mail()

        self.add_mail_to_inbox(input_mail)
        self.add_mail_to_inbox(input_mail2)

        mails = self.get_mails_by_tag('inbox')

        self.assertNotIn('read', mails[0].status)
        self.assertNotIn('read', mails[1].status)

        self.mark_many_as_read([input_mail.ident, input_mail2.ident])

        mails = self.get_mails_by_tag('inbox')

        self.assertIn('read', mails[0].status)
        self.assertIn('read', mails[1].status)
