import traceback
import sys
from app.bitmask_libraries.config import LeapConfig
from app.bitmask_libraries.provider import LeapProvider
from app.bitmask_libraries.session import LeapSessionFactory
from app.bitmask_libraries.auth import LeapCredentials


class Client:
    def __init__(self):
        try:
            self.username = 'test_user'
            self.password = 'testpassword'
            self.server_name = 'example.wazokazi.is'
            self.mailbox_name = 'inbox'
            self.leapdir = '~/.leap'

            self._open_leap_session()
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def _open_leap_session(self):
        self.leap_config = LeapConfig()
        self.provider = LeapProvider(self.server_name, self.leap_config)
        self.leap_session = LeapSessionFactory(self.provider).create(LeapCredentials(self.username, self.password))
        self.mbx = self.leap_session.account.getMailbox(self.mailbox_name)

    def mails(self, query):
        raise NotImplementedError()

    def drafts(self):
        raise NotImplementedError()

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
