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

from twisted.internet.defer import Deferred
from twisted.mail.smtp import SMTPSenderFactory
from twisted.internet import reactor
from pixelated.support.functional import flatten


class MailSender():
    def __init__(self, account_email_address, smtp_client=None):
        self.account_email_address = account_email_address

    def sendmail(self, mail):
        recipients = flatten([mail.to, mail.cc, mail.bcc])

        resultDeferred = Deferred()
        senderFactory = SMTPSenderFactory(
            fromEmail=self.account_email_address,
            toEmail=recipients,
            file=StringIO(mail.to_smtp_format()),
            deferred=resultDeferred)

        reactor.connectTCP('localhost', 4650, senderFactory)

        return resultDeferred
