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
from email.mime.text import MIMEText

from twisted.internet import defer
from twisted.trial import unittest
from twisted.mail import smtp

from mock import patch, Mock, MagicMock
from mockito import mock, when, any as ANY

from pixelated.account_recovery import AccountRecovery


class AccountRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.generated_code = '4645a2f8997e5d0d'
        self.mock_bonafide_session = Mock()
        self.mock_soledad = Mock()
        self.mock_smtp_config = Mock()
        self.keymanager = Mock()
        self.mock_smtp_config.remote_smtp_host = 'localhost'
        self.mock_soledad.create_recovery_code.return_value = self.generated_code
        self.backup_email = 'test@test.com'
        self.domain = 'test.com'
        self.account_recovery = AccountRecovery(
            self.mock_bonafide_session,
            self.mock_soledad,
            self.mock_smtp_config,
            self.backup_email,
            self.domain)
        self.mock_smtp = Mock()

    @defer.inlineCallbacks
    def test_update_recovery_code(self):
        when(self.account_recovery)._send_mail(ANY).thenReturn(defer.succeed(None))
        response = yield self.account_recovery.update_recovery_code()
        self.mock_bonafide_session.update_recovery_code.assert_called_once_with(self.generated_code)

    @defer.inlineCallbacks
    def test_send_recovery_code_by_email(self):
        sender = 'team@{}'.format(self.domain)
        msg = MIMEText('Your code %s' % self.generated_code)
        msg['Subject'] = 'Recovery Code'
        msg['From'] = sender
        msg['To'] = self.backup_email

        result = MagicMock()
        deferred_sendmail = defer.succeed(result)
        with patch.object(smtp, 'sendmail', return_value=deferred_sendmail) as mock_sendmail:
            response = yield self.account_recovery._send_mail(self.generated_code, self.backup_email)

            mock_sendmail.assert_called_with(
                self.mock_smtp_config.remote_smtp_host,
                sender,
                [self.backup_email],
                msg.as_string())
