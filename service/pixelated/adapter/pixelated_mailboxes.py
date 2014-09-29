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
from pixelated.adapter.pixelated_mailbox import PixelatedMailbox


class PixelatedMailBoxes():

    def __init__(self, account):
        self.account = account

    def _create_or_get(self, mailbox_name):
        mailbox_name = mailbox_name.upper()
        if mailbox_name not in self.account.mailboxes:
            self.account.addMailbox(mailbox_name)
        return PixelatedMailbox.create(mailbox_name)

    def drafts(self):
        return self._create_or_get('DRAFTS')

    def trash(self):
        return self._create_or_get('TRASH')

    def sent(self):
        return self._create_or_get('SENT')

    @property
    def mailboxes(self):
        return [PixelatedMailbox.create(leap_mailbox_name) for leap_mailbox_name in
                self.account.mailboxes]

    def mails_by_tag(self, query_tags):
        mails = []
        for mailbox in self.mailboxes:
            mails.extend(mailbox.mails_by_tags(query_tags))

        return mails

    def add_draft(self, mail):
        self.drafts().add(mail)
        return mail

    def update_draft(self, ident, new_version):
        new_mail = self.add_draft(new_version)
        self.drafts().remove(ident)
        return new_mail

    def move_to_trash(self, mail):
        origin_mailbox = mail.mailbox_name

        new_mail_id = self.trash().add(mail)
        self._create_or_get(origin_mailbox).remove(mail)
        return new_mail_id

    def mail(self, mail_id):
        for mailbox in self.mailboxes:
            mail = mailbox.mail(mail_id)
            if mail:
                return mail
