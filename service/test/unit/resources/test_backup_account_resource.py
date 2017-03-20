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

from mock import MagicMock, patch
from twisted.trial import unittest
from twisted.web.test.requesthelper import DummyRequest
from twisted.internet import defer

from pixelated.resources.backup_account_resource import BackupAccountResource
from test.unit.resources import DummySite


class TestBackupAccountResource(unittest.TestCase):
    def setUp(self):
        self.services_factory = MagicMock()
        self.resource = BackupAccountResource(self.services_factory, MagicMock())
        self.web = DummySite(self.resource)

    def test_get(self):
        request = DummyRequest(['/backup-account'])
        request.method = 'GET'
        d = self.web.get(request)

        def assert_200_when_user_logged_in(_):
            self.assertEqual(200, request.responseCode)
            self.assertIn("DOCTYPE html", request.written[0])

        d.addCallback(assert_200_when_user_logged_in)
        return d

    @patch('pixelated.resources.backup_account_resource.AccountRecovery')
    def test_post_updates_recovery_code(self, mock_account_recovery_init):
        mock_account_recovery = MagicMock()
        mock_account_recovery_init.return_value = mock_account_recovery
        mock_account_recovery.update_recovery_code.return_value = defer.succeed("Success")
        request = DummyRequest(['/backup-account'])
        request.method = 'POST'
        d = self.web.get(request)

        def assert_update_recovery_code_called(_):
            mock_account_recovery_init.assert_called_with(
                self.resource._authenticator.bonafide_session,
                self.resource.soledad(request))
            mock_account_recovery.update_recovery_code.assert_called()

        d.addCallback(assert_update_recovery_code_called)
        return d

    @patch('pixelated.resources.backup_account_resource.AccountRecovery.update_recovery_code')
    def test_post_returns_successfully(self, mock_update_recovery_code):
        mock_update_recovery_code.return_value = defer.succeed("Success")
        request = DummyRequest(['/backup-account'])
        request.method = 'POST'
        d = self.web.get(request)

        def assert_successful_response(_):
            self.assertEqual(204, request.responseCode)

        d.addCallback(assert_successful_response)
        return d

    @patch('pixelated.resources.backup_account_resource.AccountRecovery.update_recovery_code')
    def test_post_returns_internal_server_error(self, mock_update_recovery_code):
        mock_update_recovery_code.return_value = defer.fail(Exception)
        request = DummyRequest(['/backup-account'])
        request.method = 'POST'
        d = self.web.get(request)

        def assert_successful_response(_):
            self.assertEqual(500, request.responseCode)

        d.addCallback(assert_successful_response)
        return d
