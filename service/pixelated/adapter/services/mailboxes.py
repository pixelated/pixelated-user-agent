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
from pixelated.adapter.services.mailbox import Mailbox
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener


class Mailboxes():

    def __init__(self, account, soledad_querier):
        self.account = account
        self.querier = soledad_querier
        for mailbox_name in account.mailboxes:
            MailboxIndexerListener.listen(self.account, mailbox_name, soledad_querier)

    def _create_or_get(self, mailbox_name):
        mailbox_name = mailbox_name.upper()
        if mailbox_name not in self.account.mailboxes:
            self.account.addMailbox(mailbox_name)
        MailboxIndexerListener.listen(self.account, mailbox_name, self.querier)
        return Mailbox.create(mailbox_name, self.querier)

    def inbox(self):
        return self._create_or_get('INBOX')

    def drafts(self):
        return self._create_or_get('DRAFTS')

    def trash(self):
        return self._create_or_get('TRASH')

    def sent(self):
        return self._create_or_get('SENT')

    def mailboxes(self):
        return [self._create_or_get(leap_mailbox_name) for leap_mailbox_name in self.account.mailboxes]

    def move_to_trash(self, mail_id):
        mail = self.querier.mail(mail_id)
        mail.remove_all_tags()
        mail.set_mailbox(self.trash().mailbox_name)
        mail.save()
        return mail

    def mail(self, mail_id):
        return self.querier.mail(mail_id)
