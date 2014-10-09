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


class DeleteMailTest(unittest.TestCase, SoledadTestBase):

    def setUp(self):
        self.setup_soledad()

    def tearDown(self):
        self.teardown_soledad()

    def test_move_mail_to_trash_when_deleting(self):
        mail = MailBuilder().with_subject('Mail with tags').build_input_mail()
        self.pixelated_mailboxes.inbox().add(mail)

        inbox_mails = self.get_mails_by_tag('inbox')
        self.assertEquals(1, len(inbox_mails))

        self.delete_mail(mail.ident)

        inbox_mails = self.get_mails_by_tag('inbox')
        self.assertEquals(0, len(inbox_mails))
        trash_mails = self.get_mails_by_tag('trash')
        self.assertEquals(1, len(trash_mails))
