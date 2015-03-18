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
from test.support.integration import SoledadTestBase, MailBuilder
import os
import json


class ContactsTest(SoledadTestBase):

    def test_TO_CC_and_BCC_fields_are_being_searched(self):
        input_mail = MailBuilder().with_tags(['important']).build_input_mail()
        self.add_mail_to_inbox(input_mail)

        d = self.get_contacts(query='recipient')

        def _assert(contacts):
            self.assertTrue('recipient@to.com' in contacts)
            self.assertTrue('recipient@cc.com' in contacts)
            self.assertTrue('recipient@bcc.com' in contacts)
        d.addCallback(_assert)
        return d

    def test_FROM_address_is_being_searched(self):
        input_mail = MailBuilder().with_tags(['important']).build_input_mail()
        self.add_mail_to_inbox(input_mail)

        d = self.get_contacts(query='Sender')

        def _assert(contacts):
            self.assertIn('Formatted Sender <sender@from.com>', contacts)
        d.addCallback(_assert)
        return d

    def test_trash_and_drafts_mailboxes_are_being_ignored(self):
        self.add_multiple_to_mailbox(1, mailbox='INBOX', to='recipient@inbox.com')
        self.add_multiple_to_mailbox(1, mailbox='DRAFTS', to='recipient@drafts.com')
        self.add_multiple_to_mailbox(1, mailbox='SENT', to='recipient@sent.com')
        self.add_multiple_to_mailbox(1, mailbox='TRASH', to='recipient@trash.com')

        d = self.get_contacts(query='recipient')

        def _assert(contacts):
            self.assertTrue('recipient@inbox.com' in contacts)
            self.assertTrue('recipient@sent.com' in contacts)
            self.assertFalse('recipient@drafts.com' in contacts)
            self.assertFalse('recipient@trash.com' in contacts)
        d.addCallback(_assert)
        return d

    def test_deduplication_on_same_mail_address_using_largest(self):
        input_mail = MailBuilder().with_tags(['important']).build_input_mail()

        formatted_input_mail = MailBuilder().with_tags(['important'])
        formatted_input_mail.with_to('Recipient Principal <recipient@to.com>')
        formatted_input_mail.with_cc('Recipient Copied <recipient@cc.com>')
        formatted_input_mail.with_bcc('Recipient Carbon <recipient@bcc.com>')
        formatted_input_mail = formatted_input_mail.build_input_mail()

        self.add_mail_to_inbox(input_mail)
        self.add_mail_to_inbox(formatted_input_mail)

        d = self.get_contacts(query='Recipient')

        def _assert(contacts):
            self.assertEquals(3, len(contacts))
            self.assertTrue('Recipient Principal <recipient@to.com>' in contacts)
            self.assertTrue('Recipient Copied <recipient@cc.com>' in contacts)
            self.assertTrue('Recipient Carbon <recipient@bcc.com>' in contacts)
        d.addCallback(_assert)
        return d

    def test_bounced_addresses_are_ignored(self):
        to_be_bounced = MailBuilder().with_to('this_mail_was_bounced@domain.com').build_input_mail()
        self.add_mail_to_inbox(to_be_bounced)

        bounced_mail_template = MailBuilder().build_input_mail()
        bounced_mail = self.mailboxes.inbox().add(bounced_mail_template)
        bounced_mail.hdoc.content = self._bounced_mail_hdoc_content()
        bounced_mail.save()
        self.search_engine.index_mail(bounced_mail)

        not_bounced_mail = MailBuilder(
        ).with_tags(['important']).with_to('this_mail_was_not@bounced.com').build_input_mail()
        self.add_mail_to_inbox(not_bounced_mail)

        d = self.get_contacts(query='this')

        def _assert(contacts):
            self.assertNotIn('this_mail_was_bounced@domain.com', contacts)
            self.assertNotIn("MAILER-DAEMON@domain.org (Mail Delivery System)", contacts)
            self.assertIn('this_mail_was_not@bounced.com', contacts)
        d.addCallback(_assert)
        return d

    def _bounced_mail_hdoc_content(self):
        hdoc_file = os.path.join(os.path.dirname(__file__), '..', 'unit', 'fixtures', 'bounced_mail_hdoc.json')
        with open(hdoc_file) as f:
            hdoc = json.loads(f.read())
        return hdoc
