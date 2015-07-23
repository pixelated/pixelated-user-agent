#
# Copyright (c) 2015 ThoughtWorks, Inc.
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
from leap.mail.adaptors.soledad import SoledadMailAdaptor
from twisted.internet import defer
from pixelated.adapter.mailstore import MailStore

from leap.mail.mail import Message
from pixelated.adapter.model.mail import Mail


class LeapMail(Mail):

    def __init__(self, headers, body=None):
        self.headers = headers
        self._body = body

    @property
    def body(self):
        return self._body

class LeapMailStore(MailStore):
    __slots__ = ('account', 'soledad')

    def __init__(self, imapAccount, soledad):
        self.account = imapAccount
        self.soledad = soledad

    @defer.inlineCallbacks
    def get_mail(self, mail_id):
        try:
            message = yield SoledadMailAdaptor().get_msg_from_mdoc_id(Message, self.soledad, mail_id)

            defer.returnValue(self._leap_message_to_leap_mail(message))
        except AttributeError:
            defer.returnValue(None)

    def _leap_message_to_leap_mail(self, message):
        return LeapMail(message.get_headers())

