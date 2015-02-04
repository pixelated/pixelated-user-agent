import json
from pixelated.resources import respond_json
from twisted.web.resource import Resource


class MailTags(Resource):

    isLeaf = True

    def __init__(self, mail_id, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service
        self._mail_id = mail_id

    def render_POST(self, request):
        new_tags = json.loads(request.content.read()).get('newtags')

        try:
            mail = self._mail_service.update_tags(self._mail_id, new_tags)
        except ValueError as ve:
            return respond_json(ve.message, request, 403)
        return respond_json(mail.as_dict(), request)


class Mail(Resource):

    def __init__(self, mail_id, mail_service):
        Resource.__init__(self)
        self.putChild('tags', MailTags(mail_id, mail_service))
        self._mail_id = mail_id
        self._mail_service = mail_service

    def render_GET(self, request):
        mail = self._mail_service.mail(self._mail_id)
        return respond_json(mail.as_dict(), request)

    def render_DELETE(self, request):
        self._mail_service.delete_mail(self._mail_id)
        return respond_json(None, request)


class MailResource(Resource):

    def __init__(self, mail_service):
        Resource.__init__(self)
        self._mail_service = mail_service

    def getChild(self, mail_id, request):
        return Mail(mail_id, self._mail_service)
