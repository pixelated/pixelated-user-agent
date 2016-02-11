#
# Copyright (c) 2016 ThoughtWorks, Inc.
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

import os
from string import Template

from pixelated.resources import BaseResource
from pixelated.resources.attachments_resource import AttachmentsResource
from pixelated.resources.contacts_resource import ContactsResource
from pixelated.resources.features_resource import FeaturesResource
from pixelated.resources.feedback_resource import FeedbackResource
from pixelated.resources.login_resource import LoginResource
from pixelated.resources.logout_resource import LogoutResource
from pixelated.resources.user_settings_resource import UserSettingsResource
from pixelated.resources.mail_resource import MailResource
from pixelated.resources.mails_resource import MailsResource
from pixelated.resources.tags_resource import TagsResource
from pixelated.resources.keys_resource import KeysResource
from twisted.web.resource import Resource
from twisted.web.static import File


MODE_STARTUP = 1
MODE_RUNNING = 2


class RootResource(BaseResource):

    def __init__(self, services_factory):
        BaseResource.__init__(self, services_factory)
        self._startup_assets_folder = self._get_startup_folder()
        self._static_folder = self._get_static_folder()
        self._html_template = open(os.path.join(self._static_folder, 'index.html')).read()
        self._services_factory = services_factory
        self._startup_mode()

    def _startup_mode(self):
        self.putChild('startup-assets', File(self._startup_assets_folder))
        self._mode = MODE_STARTUP

    def getChild(self, path, request):
        if path == '':
            return self
        return Resource.getChild(self, path, request)

    def initialize(self, portal=None, disclaimer_banner=None):
        self.putChild('assets', File(self._static_folder))
        self.putChild('keys', KeysResource(self._services_factory))
        self.putChild(AttachmentsResource.BASE_URL, AttachmentsResource(self._services_factory))
        self.putChild('contacts', ContactsResource(self._services_factory))
        self.putChild('features', FeaturesResource(portal))
        self.putChild('tags', TagsResource(self._services_factory))
        self.putChild('mails', MailsResource(self._services_factory))
        self.putChild('mail', MailResource(self._services_factory))
        self.putChild('feedback', FeedbackResource(self._services_factory))
        self.putChild('user-settings', UserSettingsResource(self._services_factory))
        self.putChild(LoginResource.BASE_URL, LoginResource(self._services_factory, portal, disclaimer_banner=disclaimer_banner))
        self.putChild(LogoutResource.BASE_URL, LogoutResource(self._services_factory))

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
            account_email = self.mail_service(request).account_email
            response = Template(self._html_template).safe_substitute(account_email=account_email)
            return str(response)
