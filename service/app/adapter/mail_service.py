import traceback
import sys
import os
from twisted.internet import defer
from app.bitmask_libraries.config import LeapConfig
from app.bitmask_libraries.provider import LeapProvider
from app.bitmask_libraries.session import LeapSessionFactory
from app.bitmask_libraries.auth import LeapCredentials
from app.adapter.pixelated_mail import PixelatedMail
from app.tags import Tags


class MailService:

    def __init__(self):
        try:
            self.username = 'testuser_a003'
            self.password = 'testpassword'
            self.server_name = 'example.wazokazi.is'
            self.mailbox_name = 'INBOX'
            self.certs_home = os.path.join(os.path.abspath("."), "leap")
            self.tags = Tags()
            self._open_leap_session()
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def _open_leap_session(self):
        self.leap_config = LeapConfig(certs_home=self.certs_home)
        self.provider = LeapProvider(self.server_name, self.leap_config)
        self.leap_session = LeapSessionFactory(self.provider).create(LeapCredentials(self.username, self.password))
        self.account = self.leap_session.account
        self.mailbox = self.account.getMailbox(self.mailbox_name)

    def mails(self, query):
        mails = self.mailbox.messages or []
        mails = [PixelatedMail(mail) for mail in mails]
        return mails

    def update_tags(self, mail_id, new_tags):
        mail = self.mail(mail_id)
        new_tags = mail.update_tags(new_tags)
        self._update_flags(new_tags, mail_id)
        self._update_tag_list(new_tags)
        return new_tags

    def _update_tag_list(self, tags):
        for tag in tags:
            self.tags.add(tag)

    def _update_flags(self, new_tags, mail_id):
        new_tags_flag_name = ['tag_' + tag.name for tag in new_tags]
        self.set_flags(mail_id, new_tags_flag_name)

    def set_flags(self, mail_id, new_tags_flag_name):
        observer = defer.Deferred()
        self.mailbox.messages.set_flags(self.mailbox, [mail_id], tuple(new_tags_flag_name), 1, observer)

    def mail(self, mail_id):
        for message in self.mailbox.messages:
            if message.getUID() == int(mail_id):
                return PixelatedMail(message)

    def all_tags(self):
        return self.tags

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
