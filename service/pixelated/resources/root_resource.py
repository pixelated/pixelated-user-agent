import os
import requests
from string import Template
from pixelated.resources.attachments_resource import AttachmentsResource
from pixelated.resources.contacts_resource import ContactsResource
from pixelated.resources.features_resource import FeaturesResource
from pixelated.resources.feedback_resource import FeedbackResource
from pixelated.resources.user_settings_resource import UserSettingsResource
from pixelated.resources.mail_resource import MailResource
from pixelated.resources.mails_resource import MailsResource
from pixelated.resources.tags_resource import TagsResource
from pixelated.resources.keys_resource import KeysResource
from twisted.web.resource import Resource
from twisted.web.static import File


MODE_STARTUP = 1
MODE_RUNNING = 2


class RootResource(Resource):

    def __init__(self):
        Resource.__init__(self)
        self._startup_assets_folder = self._get_startup_folder()
        self._static_folder = self._get_static_folder()
        self._html_template = open(os.path.join(self._static_folder, 'index.html')).read()
        self._startup_mode()

    def _startup_mode(self):
        self.putChild('startup-assets', File(self._startup_assets_folder))
        self._mode = MODE_STARTUP

    def getChild(self, path, request):
        if path == '':
            return self
        return Resource.getChild(self, path, request)

    def initialize(self, keymanager, search_engine, mail_service, draft_service, feedback_service):
        self.account_email = mail_service.account_email

        self.putChild('assets', File(self._static_folder))
        self.putChild('keys', KeysResource(keymanager))
        self.putChild(AttachmentsResource.BASE_URL, AttachmentsResource(mail_service))
        self.putChild('contacts', ContactsResource(search_engine))
        self.putChild('features', FeaturesResource())
        self.putChild('tags', TagsResource(search_engine))
        self.putChild('mails', MailsResource(mail_service, draft_service))
        self.putChild('mail', MailResource(mail_service))
        self.putChild('feedback', FeedbackResource(feedback_service))
        self.putChild('user-settings', UserSettingsResource(self.account_email))

        self._mode = MODE_RUNNING

    def _get_startup_folder(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(path, '..', 'assets')

    def _get_static_folder(self):
        static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
        # this is a workaround for packaging
        if not os.path.exists(static_folder):
            static_folder = os.path.abspath(
                os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", "web-ui", "app"))
        if not os.path.exists(static_folder):
            static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')
        return static_folder

    def _is_starting(self):
        return self._mode == MODE_STARTUP

    def render_GET(self, request):
        if self._is_starting():
            return open(os.path.join(self._startup_assets_folder, 'Interstitial.html')).read()
        else:
            response = Template(self._html_template).safe_substitute(account_email=self.account_email)
            return str(response)
