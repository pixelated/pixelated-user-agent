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
from pixelated.adapter.pixelated_mail import PixelatedMail


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
        return self.account.getMailbox(self.mailbox_name)

    def mails(self, query):
        mails = self.mailbox.messages or []
        mails = [PixelatedMail.from_leap_mail(mail) for mail in mails]
        return mails

    def update_tags(self, mail_id, new_tags):
        mail = self.mail(mail_id)
        new_tags = mail.update_tags(new_tags)
        self._update_flags(new_tags, mail_id)
        self._update_tag_list(new_tags)
        return new_tags

    def _update_tag_list(self, tags):
        for tag in tags:
            pass
            # self.tags.add(tag)

    def _update_flags(self, new_tags, mail_id):
        new_tags_flag_name = ['tag_' + tag.name for tag in new_tags if tag.name not in ['inbox', 'drafts', 'sent', 'trash']]
        self.set_flags(mail_id, new_tags_flag_name)

    def set_flags(self, mail_id, new_tags_flag_name):
        observer = defer.Deferred()
        self.mailbox.messages.set_flags(self.mailbox, [mail_id], tuple(new_tags_flag_name), 1, observer)

    def mail(self, mail_id):
        for message in self.mailbox.messages:
            if message.getUID() == int(mail_id):
                return PixelatedMail.from_leap_mail(message)

    def all_tags(self):
        return []

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
