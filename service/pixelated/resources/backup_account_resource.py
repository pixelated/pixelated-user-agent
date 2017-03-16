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
from xml.sax import SAXParseException

from pixelated.resources import BaseResource
from twisted.python.filepath import FilePath
from pixelated.resources import get_protected_static_folder
from pixelated.account_recovery import AccountRecovery
from twisted.web.http import OK, NO_CONTENT, INTERNAL_SERVER_ERROR
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import Element, XMLFile, renderElement


class BackupAccountPage(Element):
    loader = XMLFile(FilePath(os.path.join(get_protected_static_folder(), 'backup_account.html')))

    def __init__(self):
        super(BackupAccountPage, self).__init__()


class BackupAccountResource(BaseResource):
    isLeaf = True

    def __init__(self, services_factory, authenticator):
        BaseResource.__init__(self, services_factory)
        self._authenticator = authenticator

    def render_GET(self, request):
        request.setResponseCode(OK)
        return self._render_template(request)

    def _render_template(self, request):
        site = BackupAccountPage()
        return renderElement(request, site)

    def render_POST(self, request):
        account_recovery = AccountRecovery(self._authenticator.bonafide_session)

        def update_response(response):
            request.setResponseCode(NO_CONTENT)
            request.finish()

        def error_response(response):
            request.setResponseCode(INTERNAL_SERVER_ERROR)
            request.finish()

        d = account_recovery.update_recovery_code()
        d.addCallbacks(update_response, error_response)
        return NOT_DONE_YET
