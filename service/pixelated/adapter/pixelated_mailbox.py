
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
from pixelated.adapter.tag import Tag


class PixelatedMailbox:

    SPECIAL_TAGS = ['inbox', 'sent', 'drafts', 'trash']

    def __init__(self, leap_mailbox):
        self.leap_mailbox = leap_mailbox

    @property
    def messages(self):
        return self.leap_mailbox.messages

    def mails(self):


        mails = self.leap_mailbox.messages or []
        mails = [PixelatedMail.from_leap_mail(mail) for mail in mails]
        return mails

    def mails_by_tags(self, tags):
        if 'all' in map(str, tags):
            return self.mails()

        return [mail for mail in self.mails() if len(mail.tags.intersection(tags)) > 0]

    def mail(self, mail_id):
        for message in self.leap_mailbox.messages:
            if message.getUID() == int(mail_id):
                return PixelatedMail.from_leap_mail(message)

    def all_tags(self):
        return Tag.from_flags(self._getFlags())

    def _getFlags(self):
        # XXX Temporary workaround while getFlags from leap is disabled
        mbox = self.leap_mailbox._get_mbox_doc()
        if not mbox:
            return self.leap_mailbox.getFlags()
        return mbox.content.get(self.leap_mailbox.FLAGS_KEY, [])

    def update_tags(self, tags):
        new_flags = set(tag.to_flag() for tag in tags)
        current_flags = set(self._getFlags())

        flags = tuple(current_flags.union(new_flags))
        self.leap_mailbox.setFlags(flags)

    @classmethod
    def create(cls, account, mailbox_name='INBOX'):
        return PixelatedMailbox(account.getMailbox(mailbox_name))
