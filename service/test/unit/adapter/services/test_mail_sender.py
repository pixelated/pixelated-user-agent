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
from leap.mail.outgoing.service import OutgoingMail
from twisted.trial import unittest

from mockito import mock, when, verify, any, unstub
from pixelated.adapter.services.mail_sender import LocalSmtpMailSender, SMTPDownException, MailSender
from pixelated.adapter.model.mail import InputMail
from pixelated.support.functional import flatten
from test.support.test_helper import mail_dict
from twisted.internet import reactor, defer
from twisted.internet.defer import Deferred


class MailSenderTest(unittest.TestCase):

    def setUp(self):
        self._cert_path = u'/some/cert/path'
        self._keymanager_mock = mock()
        self._remote_smtp_host = 'some.host.test'
        self._remote_smtp_port = 1234

    def tearDown(self):
        unstub()

    def test_iterates_over_recipients(self):
        sender = MailSender('someone@somedomain.tld', self._keymanager_mock, self._cert_path, self._remote_smtp_host, self._remote_smtp_port)
        input_mail = InputMail.from_dict(mail_dict())

        when(OutgoingMail).send_message(any(), any()).thenAnswer(lambda: defer.succeed(None))

        sender.sendmail(input_mail)

        for recipient in flatten([input_mail.to, input_mail.cc, input_mail.bcc]):
            verify(OutgoingMail).send_message(any(), recipient)


class LocalSmtpMailSenderTest(unittest.TestCase):
    def setUp(self):
        self.smtp = mock()
        self.smtp.local_smtp_port_number = 4650
        self.smtp.ensure_running = lambda: True

    def test_sendmail(self):
        when(reactor).connectTCP('localhost', 4650, any()).thenReturn(None)
        input_mail = InputMail.from_dict(mail_dict())
        mail_sender = LocalSmtpMailSender('someone@somedomain.tld', self.smtp)

        return self._succeed(mail_sender.sendmail(input_mail))

    def tearDown(self):
        unstub()

    def test_sendmail_uses_twisted(self):
        when(reactor).connectTCP('localhost', 4650, any()).thenReturn(None)

        input_mail = InputMail.from_dict(mail_dict())

        mail_sender = LocalSmtpMailSender('someone@somedomain.tld', self.smtp)

        sent_deferred = mail_sender.sendmail(input_mail)

        verify(reactor).connectTCP('localhost', 4650, any())

        return self._succeed(sent_deferred)

    def test_senmail_returns_deffered(self):
        when(reactor).connectTCP('localhost', 4650, any()).thenReturn(None)
        input_mail = InputMail.from_dict(mail_dict())
        mail_sender = LocalSmtpMailSender('someone@somedomain.tld', self.smtp)

        deferred = mail_sender.sendmail(input_mail)

        self.assertIsNotNone(deferred)
        self.assertTrue(isinstance(deferred, Deferred))

        return self._succeed(deferred)

    def test_doesnt_send_mail_if_smtp_is_not_running(self):
        self.smtp.ensure_running = lambda: False
        mail_sender = LocalSmtpMailSender('someone@somedomain.tld', self.smtp)

        deferred = mail_sender.sendmail({})

        def _assert(_):
            self.assertTrue(isinstance(deferred.result.value, SMTPDownException))

        deferred.addErrback(_assert)

        return deferred

    def _succeed(self, deferred):
        deferred.callback(None)
        return deferred
