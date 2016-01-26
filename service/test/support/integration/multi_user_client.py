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
import json
import shutil

from leap.exceptions import SRPAuthenticationError
from leap.mail.imap.account import IMAPAccount
from mockito import mock, when, any as ANY
from twisted.cred import portal
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.internet import defer

from leap.auth import SRPAuth

from pixelated.adapter.mailstore.leap_attachment_store import LeapAttachmentStore
from pixelated.adapter.services.feedback_service import FeedbackService
from pixelated.application import UserAgentMode, ServicesFactory, set_up_protected_resources

from pixelated.adapter.mailstore import LeapMailStore
from pixelated.adapter.mailstore.searchable_mailstore import SearchableMailStore

from pixelated.adapter.search import SearchEngine
from pixelated.adapter.services.draft_service import DraftService
from pixelated.bitmask_libraries.session import LeapSession, LeapSessionFactory
from pixelated.config import services as config_services
# from pixelated.config.services import Services
from pixelated.resources.auth import LeapPasswordChecker, SessionChecker, PixelatedRealm, PixelatedAuthSessionWrapper
from pixelated.resources.login_resource import LoginResource
from pixelated.resources.root_resource import RootResource
from test.support.integration import AppTestClient
from test.support.integration.app_test_client import initialize_soledad

from test.support.test_helper import request_mock


class MultiUserClient(AppTestClient):

    @defer.inlineCallbacks
    def start_client(self):
        self.soledad_test_folder = self._generate_soledad_test_folder_name()
        SearchEngine.DEFAULT_INDEX_HOME = self.soledad_test_folder
        self.cleanup = lambda: shutil.rmtree(self.soledad_test_folder)
        self.soledad = yield initialize_soledad(tempdir=self.soledad_test_folder)

        self.service_factory = ServicesFactory(UserAgentMode(is_single_user=False))

        root_resource = RootResource(self.service_factory)
        leap_provider = mock()
        self.resource = set_up_protected_resources(root_resource, leap_provider, self.service_factory)

    @defer.inlineCallbacks
    def login(self, username='username', password='password'):
        leap_session = mock(LeapSession)
        user_auth = mock()
        user_auth.uuid = 'some_user_uuid'
        leap_session.user_auth = user_auth
        config = mock()
        config.leap_home = 'some_folder'
        leap_session.config = config
        leap_session.fresh_account = False

        self._set_leap_srp_auth(username, password)
        when(LeapSessionFactory).create(username, password).thenReturn(leap_session)
        _services = yield self.generate_services()
        when(config_services).Services(leap_session).thenReturn(_services)
        # when(Services).setup().thenReturn(defer.succeed('mocked so irrelevant'))

        request = request_mock(path='/login', method="POST", body={'username': username, 'password': password})
        defer.returnValue(self._render(request, as_json=False))

    def _set_leap_srp_auth(self, username, password):
        auth_dict = {'username': 'password'}
        if auth_dict[username] == password:
            when(SRPAuth).authenticate(username, password).thenReturn(True)
        else:
            when(SRPAuth).authenticate(username, password).thenRaise(SRPAuthenticationError())

    def get(self, path, get_args='', as_json=True, from_request=None):
        request = request_mock(path)
        request.args = get_args
        if from_request:
            session = from_request.getSession()
            request.session = session
        return self._render(request, as_json)

    @defer.inlineCallbacks
    def generate_services(self):
        search_engine = SearchEngine(self.INDEX_KEY, user_home=self.soledad_test_folder)
        self.mail_sender = self._create_mail_sender()

        self.mail_store = SearchableMailStore(LeapMailStore(self.soledad), search_engine)
        self.attachment_store = LeapAttachmentStore(self.soledad)

        account_ready_cb = defer.Deferred()
        self.account = IMAPAccount(self.ACCOUNT, self.soledad, account_ready_cb)
        yield account_ready_cb
        self.leap_session = mock()

        mail_service = self._create_mail_service(self.mail_sender, self.mail_store, search_engine, self.attachment_store)
        mails = yield mail_service.all_mails()
        search_engine.index_mails(mails)

        services = mock()
        services.keymanager = mock()
        services.mail_service = mail_service
        services.draft_service = DraftService(self.mail_store)
        services.search_engine = search_engine
        services.feedback_service = FeedbackService(self.leap_session)
        defer.returnValue(services)
