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


from leap.exceptions import SRPAuthenticationError
from mockito import mock, when, any as ANY
from twisted.internet import defer

from leap.auth import SRPAuth

from pixelated.application import UserAgentMode, ServicesFactory, set_up_protected_resources

from pixelated.bitmask_libraries.session import LeapSession, LeapSessionFactory
import pixelated.config.services
from pixelated.resources.root_resource import RootResource
from test.support.integration import AppTestClient
from test.support.integration.app_test_client import initialize_soledad, AppTestAccount
import test.support.mockito
from test.support.test_helper import request_mock


class MultiUserClient(AppTestClient):

    @defer.inlineCallbacks
    def start_client(self, mode=UserAgentMode(is_single_user=True)):
        self._initialize()
        self._test_account = AppTestAccount('test', self._tmp_dir.name)

        yield self._test_account.start()

        self.cleanup = lambda: self._test_account.cleanup()
        self.soledad = self._test_account.soledad

        self.service_factory = ServicesFactory(UserAgentMode(is_single_user=False))

        root_resource = RootResource(self.service_factory)
        leap_provider = mock()
        self.resource = set_up_protected_resources(root_resource, leap_provider, self.service_factory)

    def login(self, username='username', password='password'):
        leap_session = mock(LeapSession)
        user_auth = mock()
        user_auth.uuid = 'some_user_uuid'
        leap_session.user_auth = user_auth
        config = mock()
        config.leap_home = 'some_folder'
        leap_session.config = config
        leap_session.fresh_account = False

        mock_srp_auth = 'mocked so irrelevant but just need a return value'
        self._set_leap_srp_auth(username, password, mock_srp_auth)
        when(LeapSessionFactory).create(username, password, mock_srp_auth).thenReturn(leap_session)
        when(leap_session).initial_sync().thenAnswer(lambda: defer.succeed(None))
        when(pixelated.config.services).Services(ANY()).thenReturn(self._test_account.services)

        request = request_mock(path='/login', method="POST", body={'username': username, 'password': password})
        return self._render(request, as_json=False)

    def _set_leap_srp_auth(self, username, password, mock_srp_auth):
        auth_dict = {'username': 'password'}
        if auth_dict[username] == password:
            when(SRPAuth).authenticate(username, password).thenReturn(mock_srp_auth)
        else:
            when(SRPAuth).authenticate(username, password).thenRaise(SRPAuthenticationError())

    def get(self, path, get_args='', as_json=True, from_request=None):
        request = request_mock(path)
        request.args = get_args
        if from_request:
            session = from_request.getSession()
            request.session = session
        return self._render(request, as_json)
