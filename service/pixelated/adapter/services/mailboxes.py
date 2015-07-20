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
from twisted.internet import defer
from pixelated.adapter.services.mailbox import Mailbox
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener
from pixelated.adapter.model.mail import welcome_mail


class Mailboxes(object):

    def __init__(self, account, soledad_querier, search_engine):
        self.account = account
        self.querier = soledad_querier
        self.search_engine = search_engine
        # for mailbox_name in account.mailboxes:
        # MailboxIndexerListener.listen(self.account, mailbox_name, soledad_querier)

    @defer.inlineCallbacks
    def index_mailboxes(self):
        mailboxes = yield self.account.account.list_all_mailbox_names()
        yield self._index_mailboxes(mailboxes)

    @defer.inlineCallbacks
    def _index_mailboxes(self, mailboxes):
        for mailbox_name in mailboxes:
            yield MailboxIndexerListener.listen(self.account, mailbox_name, self.querier)

    @defer.inlineCallbacks
    def _create_or_get(self, mailbox_name):
        mailbox_name = mailbox_name.upper()
        # if mailbox_name not in self.account.mailboxes:
        if mailbox_name not in (yield self.account.account.list_all_mailbox_names()):
            yield self.account.addMailbox(mailbox_name)
        yield MailboxIndexerListener.listen(self.account, mailbox_name, self.querier)
        defer.returnValue(Mailbox.create(mailbox_name, self.querier, self.search_engine))

    @property
    def inbox(self):
        return self._create_or_get('INBOX')

    @property
    def drafts(self):
        return self._create_or_get('DRAFTS')

    @property
    def trash(self):
        return self._create_or_get('TRASH')

    @property
    def sent(self):
        return self._create_or_get('SENT')

    @defer.inlineCallbacks
    def mailboxes(self):
        mailboxes_names = yield self.account.account.list_all_mailbox_names()
        defer.returnValue([(yield self._create_or_get(leap_mailbox_name)) for leap_mailbox_name in mailboxes_names])

    def move_to_trash(self, mail_id):
        return self._move_to(mail_id, self.trash)

    def move_to_inbox(self, mail_id):
        return self._move_to(mail_id, self.inbox)

    @defer.inlineCallbacks
    def _move_to(self, mail_id, mailbox):
        mailbox = yield mailbox
        mail = self.querier.mail(mail_id)
        mail.set_mailbox(mailbox.mailbox_name)
        mail.save()
        defer.returnValue(mail)

    def mail(self, mail_id):
        return self.querier.mail(mail_id)

    @defer.inlineCallbacks
    def add_welcome_mail_for_fresh_user(self):
        inbox = yield self._create_or_get('INBOX')
        if inbox.fresh:
            mail = welcome_mail()
            self.inbox.add(mail)
