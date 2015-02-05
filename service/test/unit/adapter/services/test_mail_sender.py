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
from twisted.trial import unittest

from mockito import mock, when, verify, any, unstub
from pixelated.adapter.services.mail_sender import MailSender
from pixelated.adapter.model.mail import PixelatedMail, InputMail
from test.support.test_helper import mail_dict
from twisted.internet import reactor
from twisted.internet.defer import Deferred


class MailSenderTest(unittest.TestCase):
    def test_sendmail(self):
        when(reactor).connectTCP('localhost', 4650, any()).thenReturn(None)
        input_mail = InputMail.from_dict(mail_dict())
        mail_sender = MailSender('someone@somedomain.tld')

        return self._succeed(mail_sender.sendmail(input_mail))

    def tearDown(self):
        unstub()

    def test_sendmail_uses_twisted(self):
        when(reactor).connectTCP('localhost', 4650, any()).thenReturn(None)

        input_mail = InputMail.from_dict(mail_dict())
        mail_sender = MailSender('someone@somedomain.tld')

        sent_deferred = mail_sender.sendmail(input_mail)

        verify(reactor).connectTCP('localhost', 4650, any())

        return self._succeed(sent_deferred)

    def test_senmail_returns_deffered(self):
        when(reactor).connectTCP('localhost', 4650, any()).thenReturn(None)
        input_mail = InputMail.from_dict(mail_dict())
        mail_sender = MailSender('someone@somedomain.tld')

        deferred = mail_sender.sendmail(input_mail)

        self.assertIsNotNone(deferred)
        self.assertTrue(isinstance(deferred, Deferred))

        return self._succeed(deferred)

    def _succeed(self, deferred):
        deferred.callback(None)
        return deferred
