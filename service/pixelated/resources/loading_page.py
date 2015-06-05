#
# Copyright (c) 2014 ThoughtWorks, Inc.
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
from twisted.internet.threads import deferToThread
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import File


class LoadingResource(Resource):

    def __init__(self):
        Resource.__init__(self)
        self._path = os.path.dirname(os.path.abspath(__file__))
        self.putChild('assets', File(os.path.join(self._path, '..', 'assets')))

    def render_GET(self, request):

        def open_html():
            return open(os.path.join(self._path, '..', 'assets', 'Interstitial.html')).read()

        def close_request(html):
            request.responseHeaders.addRawHeader("Connection", "close")
            request.write(html)
            request.finish()

        d = deferToThread(open_html)
        d.addCallback(close_request)

        return NOT_DONE_YET

    def getChild(self, path, request):
        if path == '':
            return self
        return Resource.getChild(self, path, request)
