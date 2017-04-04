#
# Copyright (c) 2017 ThoughtWorks, Inc.
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

from pixelated.resources import BaseResource
from twisted.python.filepath import FilePath
from pixelated.resources import get_public_static_folder
from twisted.web.http import OK
from twisted.web.template import Element, XMLFile, renderElement
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer


class AccountRecoveryPage(Element):
    loader = XMLFile(FilePath(os.path.join(get_public_static_folder(), 'account_recovery.html')))

    def __init__(self):
        super(AccountRecoveryPage, self).__init__()


class AccountRecoveryResource(BaseResource):
    BASE_URL = 'account-recovery'
    isLeaf = True

    def __init__(self, services_factory):
        BaseResource.__init__(self, services_factory)

    def render_GET(self, request):
        request.setResponseCode(OK)
        return self._render_template(request)

    def _render_template(self, request):
        site = AccountRecoveryPage()
        return renderElement(request, site)

    def render_POST(self, request):
        def success_response(response):
            request.setResponseCode(OK)
            request.finish()

        def error_response(response):
            request.setResponseCode(INTERNAL_SERVER_ERROR)
            request.finish()

        d = defer.succeed('Done!')
        d.addCallbacks(success_response, error_response)
        return NOT_DONE_YET
