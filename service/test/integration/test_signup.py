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

from twisted.internet import defer

from test.support.integration.soledad_test_base import MultiUserSoledadTestBase


class SignupTest(MultiUserSoledadTestBase):

    @defer.inlineCallbacks
    def test_signup(self):
        response, first_request = yield self.app_test_client.get('/signup', as_json=False)
        response, signup_request = yield self.app_test_client.signup(session=first_request.getSession())
        yield response

        self.assertEqual(302, signup_request.responseCode)

