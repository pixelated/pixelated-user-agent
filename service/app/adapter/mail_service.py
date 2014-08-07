import traceback
import sys
import os
from app.bitmask_libraries.config import LeapConfig
from app.bitmask_libraries.provider import LeapProvider
from app.bitmask_libraries.session import LeapSessionFactory
from app.bitmask_libraries.auth import LeapCredentials


class MailService:

    SPECIAL_BOXES = ['inbox', 'sent', 'drafts', 'trash']

    def __init__(self):
        try:
            self.username = 'test_user'
            self.password = 'testpassword'
            self.server_name = 'example.wazokazi.is'
            self.mailbox_name = 'inbox'
            self.leapdir = os.path.join(os.path.abspath("."), "leap")

            self._open_leap_session()
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def _open_leap_session(self):
        self.leap_config = LeapConfig(leap_home=self.leapdir)
        self.provider = LeapProvider(self.server_name, self.leap_config)
        self.leap_session = LeapSessionFactory(self.provider).create(LeapCredentials(self.username, self.password))
        self.account = self.leap_session.account
        self.mailbox = self.account.getMailbox(self.mailbox_name)

    def mails(self, query):
        mailbox = self._switch_mailbox(query['tags'][0])
        return mailbox.messages if mailbox else []

    def _switch_mailbox(self, name):
        mailbox = None
        if name in self.SPECIAL_BOXES:
            self._create_mailbox(name)
        try:
            mailbox = self.account.getMailbox(name)
        except Exception, e:
            if not 'MailboxException' == e.__class__.__name__:
                raise e
        return mailbox

    def _create_mailbox(self, name):
        created = False
        try:
            created = self.account.addMailbox(name)
        except Exception, e:
            if not 'MailboxCollision' == e.__class__.__name__:
                raise e
        return created

    def drafts(self):
        return []

    def mail(self, mail_id):
        raise NotImplementedError()

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

    def all_tags(self):
        raise NotImplementedError()

    def all_contacts(self, query):
        raise NotImplementedError()

if __name__ == '__main__':
    print('Running Standalone')
    client = Client()
