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
import traceback
import sys
import os
from twisted.internet import defer
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.bitmask_libraries.session import LeapSessionFactory
from pixelated.bitmask_libraries.auth import LeapCredentials
from pixelated.adapter.pixelated_mailbox import PixelatedMailbox
from pixelated.adapter.tag import Tag


class MailService:

    def __init__(self, username, password, server_name):
        try:
            self.username = username
            self.password = password
            self.server_name = server_name
            self.mailbox_name = 'INBOX'
            self.certs_home = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "certificates"))
            self._open_leap_session()
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def _open_leap_session(self):
        self.leap_config = LeapConfig(certs_home=self.certs_home)
        self.provider = LeapProvider(self.server_name, self.leap_config)
        self.leap_session = LeapSessionFactory(self.provider).create(LeapCredentials(self.username, self.password))
        self.account = self.leap_session.account

    @property
    def mailbox(self):
        return PixelatedMailbox(self.account.getMailbox(self.mailbox_name))

    def mails(self, query):
        return self.mailbox.mails()

    def update_tags(self, mail_id, new_tags):
        mail = self.mail(mail_id)
        tags = set(Tag(str_tag) for str_tag in new_tags)
        current_tags, removed_tags = mail.update_tags(tags)
        self._update_mail_flags(current_tags, removed_tags, mail_id)
        self._update_mailbox_tags(tags)
        return current_tags

    def _update_mailbox_tags(self, tags):
        self.mailbox.update_tags(tags)

    def _update_mail_flags(self, current_tags, removed_tags, mail_id):
        new_flags = ['tag_' + tag.name for tag in current_tags if tag.name not in PixelatedMailbox.SPECIAL_TAGS]
        self._append_mail_flags(mail_id, new_flags)

        removed_flags = ['tag_' + tag.name for tag in removed_tags if tag.name not in PixelatedMailbox.SPECIAL_TAGS]
        self._remove_mail_flags(mail_id, removed_flags)

    def _append_mail_flags(self, mail_id, flags):
        self._set_mail_flags(mail_id, flags, 1)

    def _remove_mail_flags(self, mail_id, flags):
        self._set_mail_flags(mail_id, flags, -1)

    def _set_mail_flags(self, mail_id, flags, operation):
        observer = defer.Deferred()
        leap_mailbox = self.account.getMailbox(self.mailbox_name)
        self.mailbox.messages.set_flags(leap_mailbox, [mail_id], tuple(flags), operation, observer)

    def mail(self, mail_id):
        return self.mailbox.mail(mail_id)

    def all_tags(self):
        return self.mailbox.all_tags()

    def thread(self, thread_id):
        raise NotImplementedError()

    def mark_as_read(self, mail_id):
        raise NotImplementedError()

    def tags_for_thread(self, thread):
        raise NotImplementedError()

    def add_tag_to_thread(self, thread_id, tag):
        raise NotImplementedError()

    def remove_tag_from_thread(self, thread_id, tag):
        raise NotImplementedError()

    def delete_mail(self, mail_id):
        raise NotImplementedError()

    def save_draft(self, draft):
        raise NotImplementedError()

    def send_draft(self, draft):
        raise NotImplementedError()

    def draft_reply_for(self, mail_id):
        raise NotImplementedError()

    def all_contacts(self, query):
        raise NotImplementedError()

    def drafts(self):
        raise NotImplementedError()
