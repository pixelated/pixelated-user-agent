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

from twisted.web.static import File


class HomeController:
    def __init__(self):
        self.static_folder = self._get_static_folder()
        pass

    def _get_static_folder(self):

        static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
        # this is a workaround for packaging
        if not os.path.exists(static_folder):
            static_folder = os.path.abspath(
                os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", "web-ui", "app"))
        if not os.path.exists(static_folder):
            static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')
        return static_folder

    def home(self, request):
        request_type = request.requestHeaders.getRawHeaders('accept')[0].split(',')[0]
        response_type = request_type if request_type else "text/html"

        request.setHeader('Content-Type', response_type)
        return File('%s/' % self.static_folder, defaultType=response_type)
