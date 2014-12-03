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

from test.support.integration import *


class DraftsTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    def tearDown(self):
        SoledadTestBase.tearDown(self)

    def test_post_sends_mail_and_deletes_previous_draft_if_it_exists(self):
        # creates one draft
        first_draft = MailBuilder().with_subject('First draft').build_json()
        first_draft_ident = self.put_mail(first_draft)

        # sends an updated version of the draft
        second_draft = MailBuilder().with_subject('Second draft').with_ident(first_draft_ident).build_json()
        self.post_mail(second_draft)

        sent_mails = self.get_mails_by_tag('sent')
        drafts = self.get_mails_by_tag('drafts')

        # make sure there is one email in the sent mailbox and it is the second draft
        self.assertEquals(1, len(sent_mails))
        self.assertEquals('Second draft', sent_mails[0].subject)

        # make sure that there are no drafts in the draft mailbox
        self.assertEquals(0, len(drafts))

    def test_post_sends_mail_even_when_draft_does_not_exist(self):
        first_draft = MailBuilder().with_subject('First draft').build_json()
        self.post_mail(first_draft)

        sent_mails = self.get_mails_by_tag('sent')
        drafts = self.get_mails_by_tag('drafts')

        self.assertEquals(1, len(sent_mails))
        self.assertEquals('First draft', sent_mails[0].subject)
        self.assertEquals(0, len(drafts))

    def test_put_creates_a_draft_if_it_does_not_exist(self):
        mail = MailBuilder().with_subject('A new draft').build_json()
        self.put_mail(mail)
        mails = self.get_mails_by_tag('drafts')

        self.assertEquals('A new draft', mails[0].subject)

    def test_put_updates_draft_if_it_already_exists(self):
        draft = MailBuilder().with_subject('First draft').build_json()
        draft_ident = self.put_mail(draft)

        updated_draft = MailBuilder().with_subject('First draft edited').with_ident(draft_ident).build_json()
        self.put_mail(updated_draft)

        drafts = self.get_mails_by_tag('drafts')

        self.assertEquals(1, len(drafts))
        self.assertEquals('First draft edited', drafts[0].subject)
