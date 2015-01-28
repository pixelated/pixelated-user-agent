import json
from pixelated.adapter.model.mail import InputMail
from pixelated.resources import respond_json, respond_json_deferred
from twisted.web import server
from twisted.web.resource import Resource


def _format_exception(e):
    exception_info = map(str, list(e.args))
    return '\n'.join(exception_info)


class MailsUnreadResource(Resource):

    isLeaf = True

    def __init__(self, mail_service, search_engine):
        Resource.__init__(self)
        self._search_engine = search_engine
        self._mail_service = mail_service

    def render_POST(self, request):
        content_dict = json.load(request.content)
        idents = content_dict.get('idents')
        for ident in idents:
            mail = self._mail_service.mark_as_unread(ident)
            self._search_engine.index_mail(mail)
        return respond_json(None, request)


class MailsReadResource(Resource):

    isLeaf = True

    def __init__(self, mail_service, search_engine):
        Resource.__init__(self)
        self._search_engine = search_engine
        self._mail_service = mail_service

    def render_POST(self, request):
        content_dict = json.load(request.content)
        idents = content_dict.get('idents')
        for ident in idents:
            mail = self._mail_service.mark_as_read(ident)
            self._search_engine.index_mail(mail)
        return respond_json(None, request)


class MailsDeleteResource(Resource):

    isLeaf = True

    def __init__(self, mail_service, search_engine):
        Resource.__init__(self)
        self._mail_service = mail_service
        self._search_engine = search_engine

    def render_POST(self, request):
        idents = json.loads(request.content.read())['idents']
        for ident in idents:
            self._delete_mail(ident)
        return respond_json(None, request)

    def _delete_mail(self, mail_id):
        mail = self._mail_service.mail(mail_id)
        if mail.mailbox_name == 'TRASH':
            self._mail_service.delete_permanent(mail_id)
            self._search_engine.remove_from_index(mail_id)
        else:
            trashed_mail = self._mail_service.delete_mail(mail_id)
            self._search_engine.index_mail(trashed_mail)


class MailsResource(Resource):

    def __init__(self, search_engine, mail_service, draft_service):
        Resource.__init__(self)
        self.putChild('delete', MailsDeleteResource(mail_service, search_engine))
        self.putChild('read', MailsReadResource(mail_service, search_engine))
        self.putChild('unread', MailsUnreadResource(mail_service, search_engine))

        self._draft_service = draft_service
        self._mail_service = mail_service
        self._search_engine = search_engine

    def render_GET(self, request):
        mail_ids, total = self._search_engine.search(request.args.get('q')[0], request.args.get('w')[0], request.args.get('p')[0])
        mails = self._mail_service.mails(mail_ids)

        response = {
            "stats": {
                "total": total,
            },
            "mails": [mail.as_dict() for mail in mails]
        }

        return respond_json(response, request)

    def render_POST(self, request):
        try:
            content_dict = json.loads(request.content.read())
            _mail = InputMail.from_dict(content_dict)
            draft_id = content_dict.get('ident')
            if draft_id:
                self._search_engine.remove_from_index(draft_id)
            sendDeferred = self._mail_service.send(draft_id, _mail)

            def onSuccess(mail):
                self._search_engine.index_mail(mail)
                respond_json_deferred(mail.as_dict(), request)

            def onError(error):
                return respond_json_deferred({'message': _format_exception(error)}, request, status_code=422)

            sendDeferred.addCallback(onSuccess)
            sendDeferred.addErrback(onError)

            return server.NOT_DONE_YET
        except Exception as error:
            return respond_json({'message': _format_exception(error)}, request, status_code=422)

    def render_PUT(self, request):
        content_dict = json.loads(request.content.read())
        _mail = InputMail.from_dict(content_dict)
        draft_id = content_dict.get('ident')

        if draft_id:
            if not self._mail_service.mail_exists(draft_id):
                return respond_json("", request, status_code=422)
            pixelated_mail = self._draft_service.update_draft(draft_id, _mail)
            self._search_engine.remove_from_index(draft_id)
        else:
            pixelated_mail = self._draft_service.create_draft(_mail)
        self._search_engine.index_mail(pixelated_mail)

        return respond_json({'ident': pixelated_mail.ident}, request)
