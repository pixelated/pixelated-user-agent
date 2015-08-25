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
# MERCHANTABILITY or FITNESS FOR A PCULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import defer


class MailboxIndexerListener(object):
    """ Listens for new mails, keeping the index updated """

    SEARCH_ENGINE = None

    @classmethod
    @defer.inlineCallbacks
    def listen(cls, account, mailbox_name, mail_store):
        listener = MailboxIndexerListener(mailbox_name, mail_store)
        if listener not in (yield account.getMailbox(mailbox_name)).listeners:
            mbx = yield account.getMailbox(mailbox_name)
            mbx.addListener(listener)

    def __init__(self, mailbox_name, mail_store):
        self.mailbox_name = mailbox_name
        self.mail_store = mail_store

    @defer.inlineCallbacks
    def newMessages(self, exists, recent):
        indexed_idents = set(self.SEARCH_ENGINE.search('tag:' + self.mailbox_name.lower(), all_mails=True))
        soledad_idents = yield self.mail_store.get_mailbox_mail_ids(self.mailbox_name)
        soledad_idents = set(soledad_idents)

        missing_idents = soledad_idents.difference(indexed_idents)

        self.SEARCH_ENGINE.index_mails((yield self.mail_store.get_mails(missing_idents)))

    def __eq__(self, other):
        return other and other.mailbox_name == self.mailbox_name

    def __hash__(self):
        return self.mailbox_name.__hash__()

    def __repr__(self):
        return 'MailboxListener: ' + self.mailbox_name


@defer.inlineCallbacks
def listen_all_mailboxes(account, search_engine, mail_store):
    MailboxIndexerListener.SEARCH_ENGINE = search_engine
    mailboxes = yield account.account.list_all_mailbox_names()
    for mailbox_name in mailboxes:
        yield MailboxIndexerListener.listen(account, mailbox_name, mail_store)
