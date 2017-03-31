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

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.logger import Logger
from twisted.mail import smtp

from email.mime.text import MIMEText


log = Logger()


class AccountRecovery(object):
    def __init__(self, session, soledad, smtp_config, backup_email):
        self._bonafide_session = session
        self._soledad = soledad
        self._smtp_config = smtp_config
        self._backup_email = backup_email

    @inlineCallbacks
    def update_recovery_code(self):
        try:
            code = self._soledad.create_recovery_code()
            response = yield self._bonafide_session.update_recovery_code(code)
            yield self._send_mail(code, self._backup_email)

            returnValue(response)

        except Exception as e:
            log.error('Something went wrong when trying to save the recovery code')
            log.error(e)
            raise e

    @inlineCallbacks
    def _send_mail(self, code, backup_email):
        msg = MIMEText('Your code %s' % code)
        msg['Subject'] = 'Recovery Code'
        msg['From'] = 'team@pixelated-project.org'
        msg['To'] = backup_email

        try:
            send_mail_result = yield smtp.sendmail(
                str(self._smtp_config.remote_smtp_host),
                'team@pixelated-project.org',
                [backup_email],
                msg.as_string())
            returnValue(send_mail_result)
        except Exception as e:
            log.error('Failed trying to send the email with the recovery code')
            raise e
