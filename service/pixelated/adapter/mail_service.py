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


class MailService:
    __slots__ = ['leap_session', 'account', 'mailbox_name']

    def __init__(self, mailboxes, mail_sender):
        self.mailboxes = mailboxes
        self.mail_sender = mail_sender

    @property
    def mailbox(self):
        return self.mailboxes.inbox()

    def mails(self, query):
        _mails = None

        if not query['tags']:
            return self.mailbox.mails()

        if query['tags']:
            _mails = self.mailboxes.mails_by_tag(query['tags'])

        return sorted(_mails or [], key=lambda mail: mail.date, reverse=True)

    def update_tags(self, mail_id, new_tags):
        mail = self.mail(mail_id)
        added, removed = mail.update_tags(new_tags)
        self.mailbox.notify_tags_updated(added, removed, self.ident)
        return new_tags

    def mail(self, mail_id):
        return self.mailbox.mail(mail_id)

    def send(self, mail):
        self.mail_sender.sendmail(mail)

    def all_tags(self):
        return self.mailbox.all_tags()

    def thread(self, thread_id):
        raise NotImplementedError()

    def mark_as_read(self, mail_id):
        return self.mail(mail_id).mark_as_read()

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
