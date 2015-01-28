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

    def __init__(self, mailboxes, mail_sender, tag_service, soledad_querier):
        self.tag_service = tag_service
        self.mailboxes = mailboxes
        self.querier = soledad_querier
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
        mail.update_tags(set(new_tags))
        return mail

    def mail(self, mail_id):
        return self.querier.mail(mail_id)

    def mail_exists(self, mail_id):
        return not(not(self.querier.get_header_by_chash(mail_id)))

    def send(self, last_draft_ident, mail):
        result = self.mail_sender.sendmail(mail)

        def success(_):
            if last_draft_ident:
                self.mailboxes.drafts().remove(last_draft_ident)
            return self.mailboxes.sent().add(mail)
        result.addCallback(success)
        return result

    def mark_as_read(self, mail_id):
        return self.mail(mail_id).mark_as_read()

    def mark_as_unread(self, mail_id):
        return self.mail(mail_id).mark_as_unread()

    def delete_mail(self, mail_id):
        return self.mailboxes.move_to_trash(mail_id)

    def delete_permanent(self, mail_id):
        mail = self.mail(mail_id)
        self.querier.remove_mail(mail)
