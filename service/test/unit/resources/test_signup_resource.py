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

from mock import MagicMock
from mockito import mock
from twisted.trial import unittest
from twisted.web.resource import getChildForRequest
from twisted.web.test.requesthelper import DummyRequest

from pixelated.application import get_static_folder
from pixelated.resources.root_resource import RootResource
from pixelated.resources.signup_resource import SignupResource


class TestSignupResource(unittest.TestCase):

    def test_get_resource_for_request(self):
        public_root_resource = RootResource(mock(), get_static_folder(), public=True)
        request = DummyRequest(['signup'])
        request.addCookie = MagicMock(return_value='stubbed')
        public_root_resource.initialize(provider=mock(), authenticator=mock())
        resource = getChildForRequest(public_root_resource, request)

        self.assertIsInstance(resource, SignupResource)

    def test_get_signup_page(self):
        signup_resource = SignupResource(mock())
        request = DummyRequest(['signup'])
        response = signup_resource.render_GET(request)

        self.assertTrue(any(('signup.js' in line) for line in response))
