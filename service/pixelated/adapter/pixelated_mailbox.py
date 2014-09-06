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

import os

from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.tag import Tag
from pixelated.adapter.tag_index import TagIndex


class PixelatedMailbox:

    SPECIAL_TAGS = set([Tag('inbox', True), Tag('sent', True), Tag('drafts', True), Tag('trash', True)])

    def __init__(self, leap_mailbox, index_file_path):
        self.leap_mailbox = leap_mailbox
        self.tag_index = TagIndex(index_file_path)
        for tag in self.SPECIAL_TAGS:
            if tag not in self.tag_index.values():
                self.tag_index.set(tag)

    @property
    def messages(self):
        return self.leap_mailbox.messages

    def mails(self):
        mails = self.leap_mailbox.messages or []
        mails = [PixelatedMail.from_leap_mail(mail) for mail in mails]
        return mails

    def mails_by_tags(self, tags):
        if 'all' in tags:
            return self.mails()

        return [mail for mail in self.mails() if len(mail.tags.intersection(tags)) > 0]

    def mail(self, mail_id):
        for message in self.leap_mailbox.messages:
            if message.getUID() == int(mail_id):
                return PixelatedMail.from_leap_mail(message)

    def all_tags(self):
        return self.tag_index.values().union(self.SPECIAL_TAGS)

    def notify_tags_updated(self, added_tags, removed_tags, mail_ident):
        for removed_tag in removed_tags:
            tag = self.tag_index.get(removed_tag)
            tag.decrement(mail_ident)
            self.tag_index.set(tag)
        for added_tag in added_tags:
            tag = self.tag_index.get(added_tag) or Tag(added_tag)
            tag.increment(mail_ident)
            self.tag_index.set(tag)

    @classmethod
    def create(cls, account, mailbox_name='INBOX'):
        db_path = os.path.join(os.environ['HOME'], '.pixelated_index')
        return PixelatedMailbox(account.getMailbox(mailbox_name), db_path)
