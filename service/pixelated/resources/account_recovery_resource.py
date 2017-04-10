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
import json

from twisted.python.filepath import FilePath
from twisted.web.http import OK, INTERNAL_SERVER_ERROR, BAD_REQUEST, UNAUTHORIZED
from twisted.web.template import Element, XMLFile, renderElement
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer
from twisted.logger import Logger
from twisted.cred.error import UnauthorizedLogin

from pixelated.resources import BaseResource
from pixelated.resources import get_public_static_folder
from pixelated.account_recovery_authenticator import AccountRecoveryAuthenticator

log = Logger()


class InvalidPasswordError(Exception):
    pass


class EmptyFieldsError(Exception):
    pass


class AccountRecoveryPage(Element):
    loader = XMLFile(FilePath(os.path.join(get_public_static_folder(), 'account_recovery.html')))

    def __init__(self):
        super(AccountRecoveryPage, self).__init__()


class AccountRecoveryResource(BaseResource):
    BASE_URL = 'account-recovery'
    isLeaf = True

    def __init__(self, services_factory, provider):
        BaseResource.__init__(self, services_factory)
        self._authenticator = AccountRecoveryAuthenticator(provider)

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

        def error_response(failure):
            log.warn(failure)
            if failure.type is InvalidPasswordError or failure.type is EmptyFieldsError:
                request.setResponseCode(BAD_REQUEST)
            elif failure.type is UnauthorizedLogin:
                request.setResponseCode(UNAUTHORIZED)
            else:
                request.setResponseCode(INTERNAL_SERVER_ERROR)
            request.finish()

        d = self._handle_post(request)
        d.addCallbacks(success_response, error_response)
        return NOT_DONE_YET

    def _get_post_form(self, request):
        return json.loads(request.content.getvalue())

    def _validate_empty_fields(self, username, user_code):
        if not username or not user_code:
            raise EmptyFieldsError('The user entered an empty username or empty usercode')

    def _validate_password(self, password, confirm_password):
        if password != confirm_password or len(password) < 8 or len(password) > 9999:
            raise InvalidPasswordError('The user entered an invalid password or confirmation')

    @defer.inlineCallbacks
    def _handle_post(self, request):
        form = self._get_post_form(request)
        username = form.get('username')
        user_code = form.get('userCode')
        password = form.get('password')
        confirm_password = form.get('confirmPassword')

        self._validate_empty_fields(username, user_code)
        self._validate_password(password, confirm_password)

        user_auth = yield self._authenticator.authenticate(username, user_code)
        defer.returnValue(user_auth)
