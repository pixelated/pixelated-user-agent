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
import pixelated.adapter.soledad_querier

querier = mock()
when(pixelated.adapter.soledad_querier).get_soledad_querier_instance().thenReturn(querier)

from pixelated.adapter.listener import MailboxListener


class MailboxListenerTest(unittest.TestCase):
    def setUp(self):
        self.account = mock()
        self.account.mailboxes = []

    def test_add_itself_to_mailbox_listeners(self):
        self.account.mailboxes = ['INBOX']
        mailbox = mock()
        when(self.account).getMailbox('INBOX').thenReturn(mailbox)
        mailbox.listeners = set()
        when(mailbox).addListener = lambda x: mailbox.listeners.add(x)

        self.assertNotIn(MailboxListener('INBOX'), mailbox.listeners)

        MailboxListener.listen(self.account, 'INBOX')

        self.assertIn(MailboxListener('INBOX'), mailbox.listeners)

    def test_reindex_missing_idents(self):
        search_engine = mock()
        when(search_engine).search('tag:inbox').thenReturn(['ident1', 'ident2'])

        MailboxListener.SEARCH_ENGINE = search_engine

        listener = MailboxListener('INBOX')
        listener.querier = querier
        when(querier).get_idents_by_mailbox('INBOX').thenReturn({'ident1', 'ident2', 'missing_ident'})
        querier.used_arguments = []
        querier.mails = lambda x: querier.used_arguments.append(x)
        listener.newMessages(10, 5)

        verify(querier, times=1).get_idents_by_mailbox('INBOX')
        self.assertIn({'missing_ident'}, querier.used_arguments)
