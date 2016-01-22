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

import logging
import os
from string import Template

from twisted.cred import credentials
from twisted.internet import defer
from twisted.web.resource import IResource
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import File

from pixelated.resources import BaseResource, UnAuthorizedResource

log = logging.getLogger(__name__)


class LoginResource(BaseResource):
    BASE_URL = 'login'

    def __init__(self, services_factory, portal=None):
        BaseResource.__init__(self, services_factory)
        self._static_folder = self._get_static_folder()
        self._startup_folder = self._get_startup_folder()
        self._html_template = open(os.path.join(self._startup_folder, 'login.html')).read()
        self._portal = portal
        self.putChild('startup-assets', File(self._startup_folder))

    def set_portal(self, portal):
        self._portal = portal

    def getChild(self, path, request):
        if path == '':
            return self
        if path == 'login':
            return self
        return UnAuthorizedResource()

    def render_GET(self, request):
        response = Template(self._html_template).safe_substitute()
        return str(response)

    def render_POST(self, request):

        def render_response(response):
            request.redirect("/")
            request.finish()

        def render_error(error):
            login_form = self.render_GET(request)
            request.status = 500
            request.write('We got an error:\n')
            request.write(str(error))
            request.write(login_form)
            request.finish()

        d = self._handle_login(request)
        d.addCallbacks(render_response, render_error)

        return NOT_DONE_YET

    @defer.inlineCallbacks
    def _handle_login(self, request):
        if self.is_logged_in(request):
            defer.succeed(None)
            return
        username = request.args['username'][0]
        password = request.args['password'][0]
        creds = credentials.UsernamePassword(username, password)

        iface, leap_user, logout = yield self._portal.login(creds, None, IResource)

        # we should really check whether the response is anonymous

        yield leap_user.start_services(self._services_factory)
        leap_user.init_http_session(request)

        log.info('about to redirect to home page')

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
