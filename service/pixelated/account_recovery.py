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

import pkg_resources
import binascii

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.logger import Logger
from twisted.mail import smtp

from email import message_from_string
from email.utils import formatdate

log = Logger()


class AccountRecovery(object):
    def __init__(self, session, soledad, smtp_config, backup_email, domain, language='en-US'):
        self._bonafide_session = session
        self._soledad = soledad
        self._smtp_config = smtp_config
        self._backup_email = backup_email
        self._domain = domain
        self._language = language

    @inlineCallbacks
    def update_recovery_code(self):
        log.info('Updating user\'s recovery code')

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
        log.info('Sending mail containing the user\'s recovery code')

        sender = 'team@{}'.format(self._domain)
        msg = self._get_recovery_mail(code, sender, backup_email)

        try:
            send_mail_result = yield smtp.sendmail(
                str(self._smtp_config.remote_smtp_host),
                sender,
                [backup_email],
                msg.as_string())
            returnValue(send_mail_result)
        except Exception as e:
            log.error('Failed trying to send the email with the recovery code')
            raise e

    def _get_recovery_mail(self, code, sender, backup_email):
        recovery_mail = pkg_resources.resource_filename(
            'pixelated.assets',
            'recovery.mail.%s' % (self._language))

        with open(recovery_mail) as mail_template_file:
            return message_from_string(mail_template_file.read().format(
                domain=self._domain,
                recovery_code=binascii.hexlify(code),
                backup_email=backup_email,
                sender=sender,
                date=formatdate(localtime=True)))
