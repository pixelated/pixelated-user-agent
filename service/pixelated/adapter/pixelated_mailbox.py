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

from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.tag_service import TagService


class PixelatedMailbox:

    def __init__(self, leap_mailbox, tag_service=TagService.get_instance()):
        self.tag_service = tag_service
        self.leap_mailbox = leap_mailbox
        self.mailbox_tag = self.leap_mailbox.mbox.lower()

    @property
    def messages(self):
        return self.leap_mailbox.messages

    def add_mailbox_tag_if_not_there(self, pixelated_mail):
        if not pixelated_mail.has_tag(self.mailbox_tag):
            pixelated_mail.update_tags({self.mailbox_tag}.union(pixelated_mail.tags))
            self.tag_service.notify_tags_updated({self.mailbox_tag}, [], pixelated_mail.ident)

    def mails(self):
        mails = self.leap_mailbox.messages or []
        result = []
        for mail in mails:
            mail._collection = mails
            pixelated_mail = PixelatedMail.from_leap_mail(mail, self.leap_mailbox)
            self.add_mailbox_tag_if_not_there(pixelated_mail)
            result.append(pixelated_mail)
        return result

    def mails_by_tags(self, tags):
        if 'all' in tags:
            return self.mails()
        return [mail for mail in self.mails() if len(mail.tags.intersection(tags)) > 0]

    def mail(self, mail_id):
        for message in self.mails():
            if message.ident == mail_id:
                return message

    def add_mail(self, mail):
        original_flags = mail.leap_mail.getFlags()
        self.leap_mailbox.addMessage(mail.raw_message(), original_flags)

    @classmethod
    def create(cls, account, mailbox_name='INBOX'):
        return PixelatedMailbox(account.getMailbox(mailbox_name))
