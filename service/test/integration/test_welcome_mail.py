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

from test.support.integration import SoledadTestBase


class TestWelcomeMail(SoledadTestBase):

    def test_welcome_mail_is_added_only_once(self):
        self.mailboxes.add_welcome_mail_for_fresh_user()
        self.mailboxes.add_welcome_mail_for_fresh_user()
        inbox_mails = self.get_mails_by_tag('inbox')
        self.assertEquals(1, len(inbox_mails))

    def test_empty_mailbox_doesnt_mean_fresh_mailbox(self):
        self.mailboxes.add_welcome_mail_for_fresh_user()
        inbox_mails = self.get_mails_by_tag('inbox')
        self.delete_mail(inbox_mails[0].ident)
        self.mailboxes.add_welcome_mail_for_fresh_user()
        inbox_mails = self.get_mails_by_tag('inbox')
        self.assertEquals(0, len(inbox_mails))
