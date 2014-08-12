import os
import mailbox

from tagsset import TagsSet
from mailset import MailSet
from contacts import Contacts

class MailService:
    MAILSET_PATH = os.path.join(os.environ['HOME'], 'mailsets', 'mediumtagged')

    def __init__(self):
        self.mailset = MailSet()
        self.tagsset = TagsSet()
        self.contacts = Contacts()

    def load_mailset(self):
        mbox_filenames = [filename for filename in os.listdir(self.MAILSET_PATH) if filename.startswith('mbox')]
        boxes = (mailbox.mbox(os.path.join(self.MAILSET_PATH, mbox)) for mbox in mbox_filenames) 

        for box in boxes:
            message = box.popitem()[1]
            if message.is_multipart():
                continue
            self.mailset.add(message)
            self.tagsset.add(message)
            self.contacts.add(message)

    def mails(self, query, page, window_size):
        mails = self.mailset.values()
        mails = [mail for mail in mails if query.test(mail)]
        return mails

    def mail(self, mail_id):
        return self.mailset.get(mail_id)

    def search_contacts(self, query):
        return self.contacts.search(query)

    def mark_as_read(self, mail_id):
        self.mailset.mark_as_read(mail_id)
        self.tagsset.mark_as_read(self.mail(mail_id).tags)



