import os
from pixelated.resources.attachments_resource import AttachmentsResource
from pixelated.resources.contacts_resource import ContactsResource
from pixelated.resources.features_resource import FeaturesResource
from pixelated.resources.mail_resource import MailResource
from pixelated.resources.mails_resource import MailsResource
from pixelated.resources.sync_info_resource import SyncInfoResource
from pixelated.resources.tags_resource import TagsResource
from twisted.web.resource import Resource
from twisted.web.static import File


class RootResource(Resource):

    def __init__(self):
        Resource.__init__(self)
        self._static_folder = self._get_static_folder()

    def getChild(self, path, request):
        if path == '':
            return self
        return Resource.getChild(self, path, request)

    def initialize(self, querier, search_engine, mail_service, draft_service):
        self.putChild('assets', File(self._static_folder))
        self.putChild('attachment', AttachmentsResource(querier))
        self.putChild('contacts', ContactsResource(search_engine))
        self.putChild('features', FeaturesResource())
        self.putChild('sync_info', SyncInfoResource())
        self.putChild('tags', TagsResource(search_engine))
        self.putChild('mails', MailsResource(search_engine, mail_service, draft_service))
        self.putChild('mail', MailResource(mail_service, search_engine))

    def _get_static_folder(self):

        static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
        # this is a workaround for packaging
        if not os.path.exists(static_folder):
            static_folder = os.path.abspath(
                os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", "web-ui", "app"))
        if not os.path.exists(static_folder):
            static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')
        return static_folder

    def render_GET(self, request):
        return open(os.path.join(self._static_folder, 'index.html')).read()
