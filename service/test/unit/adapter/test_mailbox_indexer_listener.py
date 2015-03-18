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

from mockito import mock, when, verify
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener


class MailboxListenerTest(unittest.TestCase):
    def setUp(self):
        self.querier = mock()
        self.account = mock()
        self.account.mailboxes = []

    def test_add_itself_to_mailbox_listeners(self):
        self.account.mailboxes = ['INBOX']
        mailbox = mock()
        when(self.account).getMailbox('INBOX').thenReturn(mailbox)
        mailbox.listeners = set()
        when(mailbox).addListener = lambda x: mailbox.listeners.add(x)

        self.assertNotIn(MailboxIndexerListener('INBOX', self.querier), mailbox.listeners)

        MailboxIndexerListener.listen(self.account, 'INBOX', self.querier)

        self.assertIn(MailboxIndexerListener('INBOX', self.querier), mailbox.listeners)

    def test_reindex_missing_idents(self):
        search_engine = mock()
        when(search_engine).search('tag:inbox', all_mails=True).thenReturn(['ident1', 'ident2'])

        MailboxIndexerListener.SEARCH_ENGINE = search_engine

        listener = MailboxIndexerListener('INBOX', self.querier)
        when(self.querier).idents_by_mailbox('INBOX').thenReturn({'ident1', 'ident2', 'missing_ident'})
        self.querier.used_arguments = []
        self.querier.mails = lambda x: self.querier.used_arguments.append(x)
        listener.newMessages(10, 5)

        verify(self.querier, times=1).idents_by_mailbox('INBOX')
        self.assertIn({'missing_ident'}, self.querier.used_arguments)
