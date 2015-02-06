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
from pixelated.adapter.model.mail import InputMail


class MailService:
    __slots__ = ['leap_session', 'account', 'mailbox_name']

    def __init__(self, mailboxes, mail_sender, tag_service, soledad_querier, search_engine):
        self.tag_service = tag_service
        self.mailboxes = mailboxes
        self.querier = soledad_querier
        self.search_engine = search_engine
        self.mail_sender = mail_sender

    def all_mails(self):
        return self.querier.all_mails()

    def mails(self, query, window_size, page):
        mail_ids, total = self.search_engine.search(query, window_size, page)

        return self.querier.mails(mail_ids), total

    def update_tags(self, mail_id, new_tags):
        new_tags = self._filter_white_space_tags(new_tags)
        reserved_words = self.tag_service.extract_reserved(new_tags)
        if len(reserved_words):
            raise ValueError('None of the following words can be used as tags: ' + ' '.join(reserved_words))
        mail = self.mail(mail_id)
        mail.update_tags(set(new_tags))
        self.search_engine.index_mail(mail)

        return mail

    def _filter_white_space_tags(self, tags):
        return filter(bool, map(lambda e: e.strip(), tags))

    def mail(self, mail_id):
        return self.querier.mail(mail_id)

    def mail_exists(self, mail_id):
        return not(not(self.querier.get_header_by_chash(mail_id)))

    def send_mail(self, content_dict):
        mail = InputMail.from_dict(content_dict)
        draft_id = content_dict.get('ident')

        def move_to_sent(_):
            return self.move_to_sent(draft_id, mail)

        deferred = self.mail_sender.sendmail(mail)
        deferred.addCallback(move_to_sent)
        return deferred

    def move_to_sent(self, last_draft_ident, mail):
        if last_draft_ident:
            self.mailboxes.drafts().remove(last_draft_ident)
        return self.mailboxes.sent().add(mail)

    def mark_as_read(self, mail_id):
        mail = self.mail(mail_id)
        mail.mark_as_read()
        self.search_engine.index_mail(mail)

    def mark_as_unread(self, mail_id):
        mail = self.mail(mail_id)
        mail.mark_as_unread()
        self.search_engine.index_mail(mail)

    def delete_mail(self, mail_id):
        mail = self.mail(mail_id)
        if mail.mailbox_name == 'TRASH':
            self.delete_permanent(mail_id)
        else:
            trashed_mail = self.mailboxes.move_to_trash(mail_id)
            self.search_engine.index_mail(trashed_mail)

    def delete_permanent(self, mail_id):
        mail = self.mail(mail_id)
        self.search_engine.remove_from_index(mail_id)
        self.querier.remove_mail(mail)
