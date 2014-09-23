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

from pixelated.support.id_gen import gen_pixelated_uid
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.status import Status
from pixelated.adapter.tag_service import TagService
from pixelated.adapter.soledad_querier import SoledadQuerier
from crochet import wait_for


class PixelatedMailbox:

    def __init__(self, leap_mailbox, tag_service=TagService.get_instance()):
        self.tag_service = tag_service
        self.leap_mailbox = leap_mailbox
        self.mailbox_tag = self.leap_mailbox.mbox.lower()
        self.querier = SoledadQuerier.get_instance()

    @property
    def messages(self):
        return self.leap_mailbox.messages

    @property
    def mailbox_name(self):
        return self.leap_mailbox.mbox

    def add_mailbox_tag_if_not_there(self, pixelated_mail):
        if not pixelated_mail.has_tag(self.mailbox_tag):
            pixelated_mail.update_tags({self.mailbox_tag}.union(pixelated_mail.tags))
            self.tag_service.notify_tags_updated({self.mailbox_tag}, [], pixelated_mail.ident)
            pixelated_mail.mark_as_not_recent()

    def mails(self):
        _mails = self.querier.all_mails_by_mailbox(self.leap_mailbox.mbox)

        result = []
        for mail in _mails:
            self.add_mailbox_tag_if_not_there(mail)
            result.append(mail)
        return result

    def mails_by_tags(self, tags):
        if 'all' in tags:
            return self.mails()
        return [mail for mail in self.mails() if len(mail.tags.intersection(tags)) > 0]

    def mail(self, mail_id):
        for message in self.mails():
            if message.ident == mail_id:
                return message

    def add(self, mail, use_smtp_format=False):
        return self._do_add_async(mail, use_smtp_format)

    @wait_for(timeout=3.0)
    def _do_add_async(self, mail, use_smtp_format):
        raw = mail.to_smtp_format() if use_smtp_format else mail.raw_message()
        return self.leap_mailbox.messages.add_msg(raw)

    def remove(self, mail):
        mail.mark_as_deleted()

        self.leap_mailbox.expunge()

    @classmethod
    def create(cls, account, mailbox_name='INBOX'):
        return PixelatedMailbox(account.getMailbox(mailbox_name))
