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
import json
import os
from pixelated.resources.users import UsersResource

import pixelated
from pixelated.resources import BaseResource, UnAuthorizedResource, UnavailableResource
from pixelated.resources import IPixelatedSession
from pixelated.resources.attachments_resource import AttachmentsResource
from pixelated.resources.sandbox_resource import SandboxResource
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
from pixelated.resources.inbox_resource import InboxResource, MODE_STARTUP, MODE_RUNNING
from twisted.web.resource import NoResource
from twisted.web.static import File
from twisted.web.util import Redirect

from twisted.logger import Logger

logger = Logger()


class RootResource(BaseResource):

    def __init__(self, services_factory, public=False):
        BaseResource.__init__(self, services_factory)
        self._public = public
        self._assets_folder = self._get_assets_folder()
        self._startup_assets_folder = self._get_startup_folder()
        self._static_folder = self._get_static_folder()
        self._html_template = open(os.path.join(self._static_folder, 'index.html')).read()
        self._services_factory = services_factory
        with open(os.path.join(self._startup_assets_folder, 'Interstitial.html')) as f:
            self.interstitial = f.read()
        self._redirect_to_login_resource = Redirect('login')
        self._inbox_resource = InboxResource(services_factory)
        self._startup_mode()

    def _startup_mode(self):
        self.putChildProtected('assets', File(self._assets_folder))
        self.putChildPublic('startup-assets', File(self._startup_assets_folder))
        self._mode = MODE_STARTUP
        logger.debug('Root in STARTUP mode. %s' % self)

    def getChildWithDefault(self, path, request):
        self._add_csrf_cookie(request)
        if path == '':
            return self._redirect_to_login_resource if self._public else self._inbox_resource
        if self._mode == MODE_STARTUP:
            return UnavailableResource()
        if self._is_xsrf_valid(request):
            return BaseResource.getChildWithDefault(self, path, request)
        return UnAuthorizedResource()

    def _is_xsrf_valid(self, request):
        get_request = (request.method == 'GET')
        if get_request:
            return True

        xsrf_token = request.getCookie('XSRF-TOKEN')
        logger.debug('CSRF token: %s' % xsrf_token)

        ajax_request = (request.getHeader('x-requested-with') == 'XMLHttpRequest')
        if ajax_request:
            xsrf_header = request.getHeader('x-xsrf-token')
            return xsrf_header and xsrf_header == xsrf_token

        csrf_input = request.args.get('csrftoken', [None])[0] or json.loads(request.content.read()).get('csrftoken', [None])[0]
        return csrf_input and csrf_input == xsrf_token

    def putChildPublic(self, path, resource):
        return BaseResource.putChild(self, path, resource)

    def putChildProtected(self, path, resource):
        return BaseResource.putChild(self, path, UnAuthorizedResource() if self._public else resource)

    def putChild(self, path, resource):
        logger.warn('Use either `putChildPublic` or `putChildProtected` on this resource')
        return self.putChildProtected(path, resource)  # to be on the safe side

    def initialize(self, provider=None, disclaimer_banner=None, authenticator=None):
        self.putChildPublic('sandbox', SandboxResource(self._static_folder))
        self.putChildProtected('keys', KeysResource(self._services_factory))
        self.putChildProtected(AttachmentsResource.BASE_URL, AttachmentsResource(self._services_factory))
        self.putChildProtected('contacts', ContactsResource(self._services_factory))
        self.putChildProtected('features', FeaturesResource(provider))
        self.putChildProtected('tags', TagsResource(self._services_factory))
        self.putChildProtected('mails', MailsResource(self._services_factory))
        self.putChildProtected('mail', MailResource(self._services_factory))
        self.putChildProtected('feedback', FeedbackResource(self._services_factory))
        self.putChildProtected('user-settings', UserSettingsResource(self._services_factory))
        self.putChildProtected('users', UsersResource(self._services_factory))
        self.putChildPublic(LoginResource.BASE_URL,
                            LoginResource(self._services_factory, provider, disclaimer_banner=disclaimer_banner, authenticator=authenticator))
        self.putChildPublic(LogoutResource.BASE_URL, LogoutResource(self._services_factory))

        self._inbox_resource.initialize()
        self._mode = MODE_RUNNING
        logger.debug('Root in RUNNING mode. %s' % self)

    def _get_assets_folder(self):
        pixelated_path = os.path.dirname(os.path.abspath(pixelated.__file__))
        return os.path.join(pixelated_path, '..', '..', 'web-ui', 'public')

    # TODO: use the public folder for this
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
