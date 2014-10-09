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


class DraftsTest(unittest.TestCase, SoledadTestBase):

    def setUp(self):
        self.setup_soledad()

    def tearDown(self):
        self.teardown_soledad()

    def test_post_creates_a_draft_when_data_has_no_ident(self):
        mail = MailBuilder().with_subject('A new draft').build_json()

        self.post_mail(mail)
        mails = self.get_mails_by_tag('drafts')

        self.assertEquals('A new draft', mails[0].subject)

    def test_post_sends_mail_and_deletes_previous_draft_when_data_has_ident(self):
        first_draft = MailBuilder().with_subject('First draft').build_json()
        first_draft_response = self.post_mail(first_draft)
        first_draft_ident = first_draft_response.ident

        second_draft = MailBuilder().with_subject('Second draft').with_ident(first_draft_ident).build_json()
        self.post_mail(second_draft)

        sent_mails = self.get_mails_by_tag('sent')
        drafts = self.get_mails_by_tag('drafts')

        self.assertEquals(1, len(sent_mails))
        self.assertEquals('Second draft', sent_mails[0].subject)
        self.assertEquals(0, len(drafts))

    def test_update_draft(self):
        draft = MailBuilder().with_subject('First draft').build_json()
        create_draft_response = self.post_mail(draft)
        draft_ident = create_draft_response.ident

        updated_draft = MailBuilder().with_subject('First draft edited').with_ident(draft_ident).build_json()
        self.put_mail(updated_draft)

        drafts = self.get_mails_by_tag('drafts')

        self.assertEquals(1, len(drafts))
        self.assertEquals('First draft edited', drafts[0].subject)
