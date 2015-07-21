import json
from pixelated.adapter.services.mail_sender import SMTPDownException
from pixelated.adapter.model.mail import InputMail
from twisted.web.server import NOT_DONE_YET
from pixelated.resources import respond_json, respond_json_deferred
from twisted.web.resource import Resource
from twisted.web import server
from twisted.internet import defer
from leap.common.events import (
    register,
    catalog as events
)


class MailsUnreadResource(Resource):
    isLeaf = True

    def __init__(self, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service

    def render_POST(self, request):
        idents = json.load(request.content).get('idents')
        deferreds = []
        for ident in idents:
            deferreds.append(self._mail_service.mark_as_unread(ident))

        d = defer.gatherResults(deferreds, consumeErrors=True)
        d.addCallback(lambda _: respond_json_deferred(None, request))
        d.addErrback(lambda _: respond_json_deferred(None, request, status_code=500))

        return NOT_DONE_YET


class MailsReadResource(Resource):
    isLeaf = True

    def __init__(self, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service

    def render_POST(self, request):
        idents = json.load(request.content).get('idents')
        deferreds = []
        for ident in idents:
            deferreds.append(self._mail_service.mark_as_read(ident))

        d = defer.gatherResults(deferreds, consumeErrors=True)
        d.addCallback(lambda _: respond_json_deferred(None, request))
        d.addErrback(lambda _: respond_json_deferred(None, request, status_code=500))

        return NOT_DONE_YET


class MailsDeleteResource(Resource):
    isLeaf = True

    def __init__(self, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service

    def render_POST(self, request):
        idents = json.loads(request.content.read())['idents']
        for ident in idents:
            self._mail_service.delete_mail(ident)
        return respond_json(None, request)


class MailsRecoverResource(Resource):
    isLeaf = True

    def __init__(self, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service

    def render_POST(self, request):
        idents = json.loads(request.content.read())['idents']
        for ident in idents:
            self._mail_service.recover_mail(ident)
        return respond_json(None, request)


class MailsResource(Resource):

    def _register_smtp_error_handler(self):

        def on_error(event):
            delivery_error_mail = InputMail.delivery_error_template(delivery_address=event.content)
            self._mail_service.mailboxes.inbox.add(delivery_error_mail)

        register(events.SMTP_SEND_MESSAGE_ERROR, callback=on_error)

    def __init__(self, mail_service, draft_service):
        Resource.__init__(self)
        self.putChild('delete', MailsDeleteResource(mail_service))
        self.putChild('recover', MailsRecoverResource(mail_service))
        self.putChild('read', MailsReadResource(mail_service))
        self.putChild('unread', MailsUnreadResource(mail_service))

        self._draft_service = draft_service
        self._mail_service = mail_service
        self._register_smtp_error_handler()

    def render_GET(self, request):
        query, window_size, page = request.args.get('q')[0], request.args.get('w')[0], request.args.get('p')[0]
        d = self._mail_service.mails(query, window_size, page)

        d.addCallback(lambda (mails, total): {
            "stats": {
                "total": total,
            },
            "mails": [mail.as_dict() for mail in mails]
        })
        d.addCallback(lambda res: respond_json_deferred(res, request))

        return NOT_DONE_YET

    def render_POST(self, request):
        content_dict = json.loads(request.content.read())

        deferred = self._mail_service.send_mail(content_dict)

        def onSuccess(sent_mail):
            data = sent_mail.as_dict()
            respond_json_deferred(data, request)

        def onError(error):
            if isinstance(error.value, SMTPDownException):
                respond_json_deferred({'message': str(error.value)}, request, status_code=503)
            else:
                respond_json_deferred({'message': str(error)}, request, status_code=422)

        deferred.addCallback(onSuccess)
        deferred.addErrback(onError)

        return server.NOT_DONE_YET

    def render_PUT(self, request):
        content_dict = json.loads(request.content.read())
        _mail = InputMail.from_dict(content_dict)
        draft_id = content_dict.get('ident')

        def defer_response(deferred):
            deferred.addCallback(lambda pixelated_mail: respond_json_deferred({'ident': pixelated_mail.ident}, request))

        if draft_id:
            deferred_check = self._mail_service.mail_exists(draft_id)

            def return422otherwise(mail_exists):
                if not mail_exists:
                    respond_json_deferred("", request, status_code=422)
                else:
                    defer_response(self._draft_service.update_draft(draft_id, _mail))
            deferred_check.addCallback(return422otherwise)
        else:
            defer_response(self._draft_service.create_draft(_mail))

        return server.NOT_DONE_YET
