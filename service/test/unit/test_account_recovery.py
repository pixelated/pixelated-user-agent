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

from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest

from mock import patch, Mock

from pixelated.account_recovery import AccountRecovery


class AccountRecoveryTest(unittest.TestCase):

    @inlineCallbacks
    def test_update_recovery_code(self):
        mock_session = Mock()
        account_recovery = AccountRecovery(mock_session)

        yield account_recovery.update_recovery_code()
        mock_session.update_recovery_code.assert_called_once_with('123')
