import json
from pixelated.resources import respond_json
from twisted.web.resource import Resource


class MailTags(Resource):

    isLeaf = True

    def __init__(self, mail_id, mail_service, search_engine):
        Resource.__init__(self)
        self._search_engine = search_engine
        self._mail_service = mail_service
        self._mail_id = mail_id

    def render_POST(self, request):
        content_dict = json.loads(request.content.read())
        new_tags = map(lambda tag: tag.lower(), content_dict['newtags'])
        try:
            self._mail_service.update_tags(self._mail_id, new_tags)
            mail = self._mail_service.mail(self._mail_id)
            self._search_engine.index_mail(mail)
        except ValueError as ve:
            return respond_json(ve.message, request, 403)
        return respond_json(mail.as_dict(), request)


class Mail(Resource):

    def __init__(self, mail_id, mail_service, search_engine):
        Resource.__init__(self)
        self.putChild('tags', MailTags(mail_id, mail_service, search_engine))

        self._search_engine = search_engine
        self._mail_id = mail_id
        self._mail_service = mail_service

    def render_GET(self, request):
        mail = self._mail_service.mail(self._mail_id)
        return respond_json(mail.as_dict(), request)

    def render_DELETE(self, request):
        self._delete_mail(self._mail_id)
        return respond_json(None, request)

    def _delete_mail(self, mail_id):
        mail = self._mail_service.mail(mail_id)
        if mail.mailbox_name == 'TRASH':
            self._mail_service.delete_permanent(mail_id)
            self._search_engine.remove_from_index(mail_id)
        else:
            trashed_mail = self._mail_service.delete_mail(mail_id)
            self._search_engine.index_mail(trashed_mail)


class MailResource(Resource):

    def __init__(self, mail_service, search_engine):
        Resource.__init__(self)
        self._mail_service = mail_service
        self._search_engine = search_engine

    def getChild(self, mail_id, request):
        return Mail(mail_id, self._mail_service, self._search_engine)
