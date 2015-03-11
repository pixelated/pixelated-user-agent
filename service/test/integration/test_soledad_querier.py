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

import copy
import time

from test.support.integration import *
from leap.mail.imap.fields import WithMsgFields


class SoledadQuerierTest(SoledadTestBase, WithMsgFields):

    def setUp(self):
        SoledadTestBase.setUp(self)
        self.soledad = self.client.soledad
        self.maxDiff = None
        self.soledad_querier = self.client.soledad_querier

    def _get_empty_mailbox(self):
        return copy.deepcopy(self.EMPTY_MBOX)

    def _create_mailbox(self, mailbox_name):
        new_mailbox = self._get_empty_mailbox()
        new_mailbox['mbox'] = mailbox_name
        new_mailbox['created'] = int(time.time() * 10E2)
        return self.soledad.create_doc(new_mailbox)

    def _get_mailboxes_from_soledad(self, mailbox_name):
        return [m for m in self.soledad.get_from_index('by-type', 'mbox') if m.content['mbox'] == mailbox_name]

    def test_remove_dup_mailboxes_keeps_the_one_with_the_highest_last_uid(self):
        self.client.add_multiple_to_mailbox(3, 'INBOX')  # by now we already have one inbox with 3 mails
        self._create_mailbox('INBOX')  # now we have a duplicate

        # make sure we have two
        inboxes = self._get_mailboxes_from_soledad('INBOX')
        self.assertEqual(2, len(inboxes))

        self.soledad_querier.remove_duplicates()

        # make sure we only have one, and the one with the right lastuid
        inboxes = self._get_mailboxes_from_soledad('INBOX')
        self.assertEqual(1, len(inboxes))
        self.assertEqual(3, inboxes[0].content['lastuid'])

    def test_all_mails_skips_incomplete_mails(self):
        # creating incomplete mail, we will only save the fdoc
        fdoc, hdoc, bdoc = MailBuilder().build_input_mail().get_for_save(1, 'INBOX')
        self.soledad.create_doc(fdoc)

        mails = self.soledad_querier.all_mails()
        self.assertEqual(0, len(mails))  # mail is incomplete since it only has fdoc

        # adding the hdoc still doesn't complete the mail
        self.soledad.create_doc(hdoc)

        mails = self.soledad_querier.all_mails()
        self.assertEqual(0, len(mails))

        # now the mail is complete
        self.soledad.create_doc(bdoc)

        mails = self.soledad_querier.all_mails()
        self.assertEqual(1, len(mails))

    def test_get_mails_by_chash(self):
        mails = self.client.add_multiple_to_mailbox(3, 'INBOX')
        chashes = [mail.ident for mail in mails]

        fetched_mails = self.soledad_querier.mails(chashes)

        self.assertEquals([m.as_dict() for m in fetched_mails], [m.as_dict() for m in mails])

    def test_empty_or_bad_queries_are_handled(self):
        self.client.add_multiple_to_mailbox(3, 'INBOX')

        test_parameters = ['', 'undefined', None, 'none']

        def call_with_bad_parameters(funct):
            for param in test_parameters:
                self.assertFalse(funct(param))

        call_with_bad_parameters(self.soledad_querier.get_all_flags_by_mbox)
        call_with_bad_parameters(self.soledad_querier.get_content_by_phash)
        call_with_bad_parameters(self.soledad_querier.get_flags_by_chash)
        call_with_bad_parameters(self.soledad_querier.get_header_by_chash)
        call_with_bad_parameters(self.soledad_querier.get_recent_by_mbox)
        call_with_bad_parameters(self.soledad_querier.idents_by_mailbox)
        call_with_bad_parameters(self.soledad_querier.get_mbox)
