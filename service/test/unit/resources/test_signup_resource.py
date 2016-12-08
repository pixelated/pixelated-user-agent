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
from mock import MagicMock, patch
from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest
from twisted.web.resource import getChildForRequest
from twisted.web.test.requesthelper import DummyRequest

import leap.common.events
from pixelated.application import get_static_folder
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.register import Credentials, register
from pixelated.resources.root_resource import RootResource
from pixelated.resources.signup_resource import SignupResource
from test.unit.resources import DummySite


class TestSignupResource(unittest.TestCase):

    def setUp(self):
        self.provider = MagicMock()
        self.provider.local_ca_crt = MagicMock()
        self.signup_resource = SignupResource(MagicMock(), self.provider)

    @patch('leap.common.events.register')
    def test_get_resource_for_request(self, *mocks):
        public_root_resource = RootResource(MagicMock(), get_static_folder(), public=True)
        request = DummyRequest(['signup'])
        request.addCookie = MagicMock(return_value='stubbed')
        public_root_resource.initialize(provider=MagicMock(), authenticator=MagicMock())
        resource = getChildForRequest(public_root_resource, request)

        self.assertIsInstance(resource, SignupResource)

    def test_get_signup_page(self):
        request = DummyRequest(['signup'])
        response = self.signup_resource.render_GET(request)

        self.assertTrue(any(('signup.js' in line) for line in response))

    @inlineCallbacks
    def test_get_signup_page2(self, *mocked):
        request = DummyRequest(['signup'])
        request.addCookie = MagicMock(return_value='stubbed')
        web = DummySite(self.signup_resource)
        request = yield web.get(request)
        self.assertTrue(any(('signup.js' in line) for line in request.written))

    @patch('pixelated.register.Api')
    @patch('pixelated.register.Session')
    @inlineCallbacks
    def test_post_to_signup_page_should_register_with_leap_provider(self, SessionMock, ApiMock):
        username, password, invite = 'roald', 'asdf123!', 'invi-1234'

        SessionMock.return_value = session = MagicMock()
        session.signup = MagicMock(return_value=(True, username))

        ApiMock.return_value = srp_provider = MagicMock()

        request = DummyRequest(['signup'])
        request.method = 'POST'
        request.content = json.dumps(dict(username=username, password=password, invite=invite))

        web = DummySite(self.signup_resource)
        request = yield web.get(request)

        self.assertTrue(SessionMock.called)
        self.assertIsInstance(SessionMock.call_args[0][0], Credentials)
        self.assertIs(SessionMock.call_args[0][1], srp_provider)
        print SessionMock.call_args[0][2], self.provider
        self.assertIs(SessionMock.call_args[0][2], self.provider.local_ca_crt)
        session.signup.assert_called_with(username, password, invite)
