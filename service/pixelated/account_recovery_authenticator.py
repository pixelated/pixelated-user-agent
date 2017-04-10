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

from leap.bitmask.bonafide.provider import Api
from leap.bitmask.bonafide.session import Session

from twisted.cred.error import UnauthorizedLogin
from twisted.internet.defer import inlineCallbacks, returnValue

from authentication import Authenticator, Authentication


class AccountRecoveryAuthenticator(Authenticator):
    def __init__(self, leap_provider):
        super(AccountRecoveryAuthenticator, self).__init__(leap_provider)

    def _auth_error(self):
        raise UnauthorizedLogin("User typed wrong recovery-code/username combination.")

    @inlineCallbacks
    def _bonafide_auth(self, credentials):
        srp_provider = Api(self._leap_provider.api_uri)
        self.bonafide_session = Session(credentials, srp_provider, self._leap_provider.local_ca_crt)
        yield self.bonafide_session.authenticate_with_recovery_code()
        returnValue(Authentication(credentials.username,
                                   self.bonafide_session.token,
                                   self.bonafide_session.uuid,
                                   'session_id',
                                   {'is_admin': False}))
