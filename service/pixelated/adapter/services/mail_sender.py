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
import re

from twisted.internet.defer import Deferred
from twisted.mail.smtp import SMTPSenderFactory
from twisted.internet import reactor
from pixelated.support.functional import flatten


class MailSender(object):
    def __init__(self, account_email_address, smtp_client=None):
        self.account_email_address = account_email_address

    def recepients_normalizer(self, mail_list):
        return set(mail_list)

    def get_email_addresses(self, mail_list):
        clean_mail_list = []
        for mail_address in mail_list:
            if "<" in mail_address:
                match = re.search(r'<(.*)>', mail_address)
                clean_mail_list.append(match.group(1))
            else:
                clean_mail_list.append(mail_address)
        return self.recepients_normalizer(clean_mail_list)

    def sendmail(self, mail):
        recipients = flatten([mail.to, mail.cc, mail.bcc])
        normalized_recipients = self.get_email_addresses(recipients)
        resultDeferred = Deferred()
        senderFactory = SMTPSenderFactory(
            fromEmail=self.account_email_address,
            toEmail=normalized_recipients,
            file=StringIO(mail.to_smtp_format()),
            deferred=resultDeferred)

        reactor.connectTCP('localhost', 4650, senderFactory)

        return resultDeferred
