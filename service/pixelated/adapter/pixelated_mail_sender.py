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
import smtplib


class PixelatedMailSender():
    def __init__(self, account_email_address):
        self.account_email_address = account_email_address
        self.smtp_client = smtplib.SMTP('localhost', 4650)

    def sendmail(self, mail):
        _from = self.account_email_address
        _to = mail.get_to()

        self.smtp_client.sendmail(_from, _to, mail.to_smtp_format(_from=_from))
