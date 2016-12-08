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
import pkg_resources

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger
from twisted.web.server import NOT_DONE_YET

from pixelated.register import register
from pixelated.resources import BaseResource

log = Logger()


class SignupResource(BaseResource):

    isLeaf = True

    def __init__(self, services_factory, provider):
        BaseResource.__init__(self, services_factory)
        self._provider = provider

    def render_GET(self, request):
        return pkg_resources.resource_stream('templates', 'signup.html')

    @inlineCallbacks
    def _render_POST(self, request):
        form_data = json.loads(request.content)
        yield register(form_data['username'], form_data['password'], self._provider, form_data['invite'])
        request.finish()

    def render_POST(self, request):
        self._render_POST(request)
        return NOT_DONE_YET
