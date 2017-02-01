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

from pixelated.resources import BaseResource, UnAuthorizedResource
from twisted.python.filepath import FilePath
from pixelated.resources import get_static_folder
from twisted.web.http import OK
from twisted.web.resource import NoResource
from twisted.web.template import Element, XMLFile, renderElement



def parse_accept_language(all_headers):
    accepted_languages = ['pt-BR', 'en-US']
    languages = all_headers.get('accept-language', '').split(';')[0]
    for language in accepted_languages:
        if language in languages:
            return language
    return 'pt-BR'



class AccountRecoveryPage(Element):
    loader = XMLFile(FilePath(os.path.join(get_static_folder(), 'account_recovery.html')))

    def __init__(self):
        super(AccountRecoveryPage, self).__init__()


class AccountRecoveryResource(BaseResource):
    BASE_URL = 'recovery'

    def __init__(self, services_factory):
        BaseResource.__init__(self, services_factory)


    def getChild(self, path, request):
        if path == BASE_URL:
            return self
        if not self.is_logged_in(request):
            return UnAuthorizedResource()
        return NoResource()

    def render_GET(self, request):
        request.setResponseCode(OK)
        return self._render_template(request)

    def _render_template(self, request):
        site = AccountRecoveryPage()
        return renderElement(request, site)
