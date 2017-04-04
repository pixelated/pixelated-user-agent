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

from mock import MagicMock
from twisted.trial import unittest
from twisted.web.test.requesthelper import DummyRequest
from twisted.internet import defer

from pixelated.resources.account_recovery_resource import AccountRecoveryResource
from test.unit.resources import DummySite


class TestAccountRecoveryResource(unittest.TestCase):
    def setUp(self):
        self.services_factory = MagicMock()
        self.resource = AccountRecoveryResource(self.services_factory)
        self.web = DummySite(self.resource)

    def test_get(self):
        request = DummyRequest(['/account-recovery'])
        request.method = 'GET'
        d = self.web.get(request)

        def assert_200_when_user_logged_in(_):
            self.assertEqual(200, request.responseCode)
            self.assertIn("DOCTYPE html", request.written[0])

        d.addCallback(assert_200_when_user_logged_in)
        return d

    def test_post_returns_successfully(self):
        request = DummyRequest(['/account-recovery'])
        request.method = 'POST'
        d = self.web.get(request)

        def assert_successful_response(_):
            self.assertEqual(200, request.responseCode)

        d.addCallback(assert_successful_response)
        return d
