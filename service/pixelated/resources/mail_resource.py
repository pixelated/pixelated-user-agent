import json
from pixelated.resources import respond_json, respond_json_deferred
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET


class MailTags(Resource):

    isLeaf = True

    def __init__(self, mail_id, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service
        self._mail_id = mail_id

    def render_POST(self, request):
        new_tags = json.loads(request.content.read()).get('newtags')

        d = self._mail_service.update_tags(self._mail_id, new_tags)
        d.addCallback(lambda mail: respond_json_deferred(mail.as_dict(), request))

        def handle403(failure):
            failure.trap(ValueError)
            return respond_json_deferred(failure.getErrorMessage(), request, 403)
        d.addErrback(handle403)
        return NOT_DONE_YET


class Mail(Resource):

    def __init__(self, mail_id, mail_service):
        Resource.__init__(self)
        self.putChild('tags', MailTags(mail_id, mail_service))
        self._mail_id = mail_id
        self._mail_service = mail_service

    def render_GET(self, request):
        d = self._mail_service.mail(self._mail_id)

        d.addCallback(lambda mail: respond_json_deferred(mail.as_dict(), request))

        return NOT_DONE_YET

    def render_DELETE(self, request):
        self._mail_service.delete_mail(self._mail_id)
        return respond_json(None, request)


class MailResource(Resource):

    def __init__(self, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service

    def getChild(self, mail_id, request):
        return Mail(mail_id, self._mail_service)
