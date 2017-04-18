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

from mock import patch, Mock
from mockito import when, any as ANY

from pixelated.account_recovery import AccountRecovery

RECOVERY_CODE_EMAIL = '''Hello,

You are receiving this email because you registered at a Pixelated provider, on test.com.
In case you ever forget your password, you can access this link test.com/account-recovery and put the following recovery code:

4645a2f8997e5d0d

This code is the only way to recover access to your account in case you lose your password.
Be careful and keep it safe!!!

Why is this so important?

Pixelated is an email client that respects your privacy and uses PGP Encryption to do so.
Your password also gives you access to your keys, so if you forget it you will lose access to your account and the ability to decrypt your messages.
We understand that forgetting passwords is a common thing, so we developed a more secure way to recover access to your account, therefore, a little bit more annoying ;)
This code is half of a big code to recover your account, the other half is with the account administrator. In case you forget your password, use this code and your administrator code to recover access to your account. It\'s like those locks with two keys :)
You will only succeed if you have both codes, so, never hurts to ask again: SAVE THIS CODE!


PS: If you didn\'t create an account at test.com, please ignore this email.
'''


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
        yield self.account_recovery.update_recovery_code()
        self.mock_bonafide_session.update_recovery_code.assert_called_once_with(self.generated_code)

    @defer.inlineCallbacks
    def test_send_recovery_code_by_email(self):
        sender = 'team@{}'.format(self.domain)
        msg = MIMEText(RECOVERY_CODE_EMAIL)
        msg['Subject'] = 'Recovery Code'
        msg['From'] = sender
        msg['To'] = self.backup_email

        with patch.object(smtp, 'sendmail', return_value=defer.succeed(None)) as mock_sendmail:
            yield self.account_recovery._send_mail(self.generated_code, self.backup_email)

            mock_sendmail.assert_called_with(
                self.mock_smtp_config.remote_smtp_host,
                sender,
                [self.backup_email],
                msg.as_string())
