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

import json
from pixelated.adapter.mail import InputMail
from pixelated.controllers import respond_json


class MailsController:

    def __init__(self, mail_service, draft_service, search_engine):
        self._mail_service = mail_service
        self._draft_service = draft_service
        self._search_engine = search_engine

    def mails(self, request):
        mail_ids, total = self._search_engine.search(request.args.get('q')[0], request.args.get('w')[0], request.args.get('p')[0])
        mails = self._mail_service.mails(mail_ids)

        response = {
            "stats": {
                "total": total,
            },
            "mails": [mail.as_dict() for mail in mails]
        }

        return json.dumps(response)

    def mail(self, request, mail_id):
        mail = self._mail_service.mail(mail_id)
        return respond_json(mail.as_dict(), request)

    def mark_mail_as_read(self, request, mail_id):
        mail = self._mail_service.mark_as_read(mail_id)
        self._search_engine.index_mail(mail)
        return ""

    def mark_mail_as_unread(self, request, mail_id):
        mail = self._mail_service.mark_as_unread(mail_id)
        self._search_engine.index_mail(mail)
        return ""

    def mark_many_mail_unread(self, request):
        content_dict = json.load(request.content)
        idents = content_dict.get('idents')
        for ident in idents:
            mail = self._mail_service.mark_as_unread(ident)
            self._search_engine.index_mail(mail)
        return ""

    def mark_many_mail_read(self, request):
        content_dict = json.load(request.content)
        idents = content_dict.get('idents')
        for ident in idents:
            mail = self._mail_service.mark_as_read(ident)
            self._search_engine.index_mail(mail)
        return ""

    def delete_mail(self, request, mail_id):
        mail = self._mail_service.mail(mail_id)
        if mail.mailbox_name == 'TRASH':
            self._mail_service.delete_permanent(mail_id)
        else:
            trashed_mail = self._mail_service.delete_mail(mail_id)
            self._search_engine.index_mail(trashed_mail)
        return respond_json(None, request)

    def delete_mails(self, request):
        idents = json.loads(request.form['idents'])
        for ident in idents:
            self.delete_mail(ident)
        return respond_json(None, request)

    def send_mail(self, request):
        try:
            content_dict = json.loads(request.content.read())
            _mail = InputMail.from_dict(content_dict)
            draft_id = content_dict.get('ident')
            if draft_id:
                self._search_engine.remove_from_index(draft_id)
            _mail = self._mail_service.send(draft_id, _mail)
            self._search_engine.index_mail(_mail)

            return respond_json(_mail.as_dict(), request)
        except Exception as error:
            return respond_json({'message': self._format_exception(error)}, request, status_code=422)

    def mail_tags(self, request, mail_id):
        content_dict = json.loads(request.content.read())
        new_tags = map(lambda tag: tag.lower(), content_dict['newtags'])
        try:
            self._mail_service.update_tags(mail_id, new_tags)
            mail = self._mail_service.mail(mail_id)
            self._search_engine.index_mail(mail)
        except ValueError as ve:
            return respond_json(ve.message, request, 403)
        return respond_json(mail.as_dict(), request)

    def update_draft(self, request):
        content_dict = json.loads(request.content.read())

        _mail = InputMail.from_dict(content_dict)
        draft_id = content_dict.get('ident')
        if draft_id:
            ident = self._draft_service.update_draft(draft_id, _mail).ident
            self._search_engine.remove_from_index(draft_id)
        else:
            ident = self._draft_service.create_draft(_mail).ident

        self._search_engine.index_mail(self._mail_service.mail(ident))
        return respond_json({'ident': ident}, request)

    def _format_exception(self, exception):
        exception_info = map(str, list(exception.args))
        return '\n'.join(exception_info)
