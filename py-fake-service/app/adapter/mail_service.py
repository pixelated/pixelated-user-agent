import os
import mailbox

from tagsset import TagsSet
from mailset import MailSet
from contacts import Contacts
from mail import Mail


class MailService:
    MAILSET_PATH = os.path.join(os.environ['HOME'], 'mailsets', 'mediumtagged')

    def __init__(self):
        self.mailset = MailSet()
        self.tagsset = TagsSet()
        self.contacts = Contacts()

    def load_mailset(self):
        mbox_filenames = [
            filename
            for filename in os.listdir
            (self.MAILSET_PATH) if filename.startswith('mbox')]
        boxes = (mailbox.mbox
                 (os.path.join(self.MAILSET_PATH, mbox))
                 for mbox in mbox_filenames)

        for box in boxes:
            message = box.popitem()[1]
            self.mailset.add(message)
            self.tagsset.add(message)
            self.contacts.add(message)

    def mails(self, query, page, window_size):
        mails = self.mailset.values()
        mails = [mail for mail in mails if query.test(mail)]
        return sorted(mails, key=lambda mail: mail.date, reverse=True)

    def mail(self, mail_id):
        return self.mailset.get(mail_id)

    def search_contacts(self, query):
        return self.contacts.search(query)

    def mark_as_read(self, mail_id):
        self.mailset.mark_as_read(mail_id)
        self.tagsset.mark_as_read(self.mail(mail_id).tags)

    def delete_mail(self, mail_id):
        purged = self.mailset.delete(mail_id)
        if not purged:
            self.tagsset.increment_tag_total_count('trash')

    def update_tags_for(self, mail_id, new_tags):
        mail = self.mail(mail_id)

        new_tags_set = set(new_tags)
        old_tags_set = set(mail.tags)

        increment_set = new_tags_set - old_tags_set
        decrement_set = old_tags_set - new_tags_set

        map(lambda x: self.tagsset.increment_tag_total_count(x), increment_set)
        map(lambda x: self.tagsset.decrement_tag_total_count(x), decrement_set)

        mail.tags = new_tags

    def send(self, mail):
        mail = Mail.from_json(mail)
        self.mailset.update(mail)
        self.tagsset.increment_tag_total_count('sent')
        self.tagsset.decrement_tag_total_count('drafts')
        return mail.ident

    def save_draft(self, mail):
        mail = self.mailset.add_draft(Mail.from_json(mail))
        return mail.ident

    def update_draft(self, mail):
        mail = Mail.from_json(mail)
        self.mailset.update(mail)
        return mail.ident

    def draft_reply_for(self, mail_id):
        return self.mailset.find(draft_reply_for=mail_id)
