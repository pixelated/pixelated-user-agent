#
# Copyright (c) 2014 ThoughtWorks, Inc.
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
from StringIO import StringIO
from email.utils import parseaddr

from twisted.internet.defer import Deferred, fail
from twisted.mail.smtp import SMTPSenderFactory
from twisted.internet import reactor
from pixelated.support.functional import flatten


class SMTPDownException(Exception):
    def __init__(self):
        Exception.__init__(self, "Couldn't send mail now, try again later.")


class MailSender(object):

    def __init__(self, account_email_address, smtp):
        self.smtp = smtp
        self.account_email_address = account_email_address

    def sendmail(self, mail):
        if self.smtp.ensure_running():
            recipients = flatten([mail.to, mail.cc, mail.bcc])
            result_deferred = Deferred()
            sender_factory = SMTPSenderFactory(
                fromEmail=self.account_email_address,
                toEmail=set([parseaddr(recipient)[1] for recipient in recipients]),
                file=StringIO(mail.to_smtp_format()),
                deferred=result_deferred)

            reactor.connectTCP('localhost', self.smtp.local_smtp_port_number,
                               sender_factory)

            return result_deferred
        return fail(SMTPDownException())
