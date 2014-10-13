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
from pixelated.adapter.tag_service import TagService
from pixelated.adapter.soledad_querier import SoledadQuerier


class MailService:
    __slots__ = ['leap_session', 'account', 'mailbox_name']

    def __init__(self, mailboxes, mail_sender, tag_service=TagService.get_instance()):
        self.tag_service = tag_service
        self.mailboxes = mailboxes
        self.querier = SoledadQuerier.get_instance()
        self.mail_sender = mail_sender

    def all_mails(self):
        return self.querier.all_mails()

    def mails(self, ids):
        return self.querier.mails(ids)

    def update_tags(self, mail_id, new_tags):
        reserved_words = self.tag_service.extract_reserved(new_tags)
        if len(reserved_words):
            raise ValueError('None of the following words can be used as tags: ' + ' '.join(reserved_words))
        mail = self.mail(mail_id)
        return mail.update_tags(set(new_tags))

    def mail(self, mail_id):
        return self.mailboxes.mail(mail_id)

    def send(self, last_draft_ident, mail):
        self.mail_sender.sendmail(mail)
        if last_draft_ident:
            self.mailboxes.drafts().remove(last_draft_ident)
        return self.mailboxes.sent().add(mail)

    def thread(self, thread_id):
        raise NotImplementedError()

    def mark_as_read(self, mail_id):
        return self.mail(mail_id).mark_as_read()

    def mark_as_unread(self, mail_id):
        return self.mail(mail_id).mark_as_unread()

    def tags_for_thread(self, thread):
        raise NotImplementedError()

    def add_tag_to_thread(self, thread_id, tag):
        raise NotImplementedError()

    def remove_tag_from_thread(self, thread_id, tag):
        raise NotImplementedError()

    def delete_mail(self, mail_id):
        return self.mailboxes.move_to_trash(mail_id)

    def save_draft(self, draft):
        raise NotImplementedError()

    def draft_reply_for(self, mail_id):
        raise NotImplementedError()

    def all_contacts(self, query):
        raise NotImplementedError()

    def drafts(self):
        raise NotImplementedError()
