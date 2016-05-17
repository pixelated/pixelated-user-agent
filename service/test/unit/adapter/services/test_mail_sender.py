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
from twisted.mail.smtp import User
from twisted.trial import unittest

from mockito import mock, when, verify, any, unstub
from pixelated.adapter.services.mail_sender import MailSender, MailSenderException
from pixelated.adapter.model.mail import InputMail
from pixelated.bitmask_libraries.smtp import LeapSMTPConfig
from pixelated.support.functional import flatten
from test.support.test_helper import mail_dict, duplicates_in_fields_mail_dict
from twisted.internet import reactor, defer
from twisted.internet.defer import Deferred
from mockito.matchers import Matcher


class TwistedSmtpUserCapture(Matcher):

    def __init__(self, username):
        self._username = username

    def matches(self, arg):
        return isinstance(arg, User) \
            and isinstance(arg.dest.addrstr, str) \
            and self._username == arg.dest.addrstr


class MailToSmtpFormatCapture(Matcher):

    def __init__(self, recipient, bccs):
        self._recipient = recipient
        self._bccs = bccs

    def matches(self, mail):
        if self._recipient in self._bccs:
            return 'Bcc: %s\n' % self._recipient in mail
        else:
            return "Bcc: " not in mail


class MailSenderTest(unittest.TestCase):

    def setUp(self):
        self._cert_path = u'/some/cert/path'
        self._keymanager_mock = mock()
        self._remote_smtp_host = 'some.host.test'
        self._remote_smtp_port = 1234
        self._smtp_config = LeapSMTPConfig('someone@somedomain.tld', self._cert_path, self._remote_smtp_host, self._remote_smtp_port)
        self.sender = MailSender(self._smtp_config, self._keymanager_mock)

    def tearDown(self):
        unstub()

    @defer.inlineCallbacks
    def test_iterates_over_recipients(self):
        input_mail = InputMail.from_dict(mail_dict(), from_address='pixelated@org')

        when(OutgoingMail).send_message(any(), any()).thenReturn(defer.succeed(None))

        yield self.sender.sendmail(input_mail)

        for recipient in flatten([input_mail.to, input_mail.cc, input_mail.bcc]):
            verify(OutgoingMail).send_message(any(), TwistedSmtpUserCapture(recipient))

    @defer.inlineCallbacks
    def test_problem_with_email_raises_exception(self):
        input_mail = InputMail.from_dict(mail_dict(), from_address='pixelated@org')

        when(OutgoingMail).send_message(any(), any()).thenReturn(defer.fail(Exception('pretend something went wrong')))

        try:
            yield self.sender.sendmail(input_mail)
            self.fail('Exception expected!')
        except MailSenderException, e:
            for recipient in flatten([input_mail.to, input_mail.cc, input_mail.bcc]):
                self.assertTrue(recipient in e.email_error_map)

    @defer.inlineCallbacks
    def test_iterates_over_recipients_and_send_whitout_bcc_field(self):
        input_mail = InputMail.from_dict(mail_dict(), from_address='pixelated@org')
        bccs = input_mail.bcc

        when(OutgoingMail).send_message(any(), any()).thenReturn(defer.succeed(None))

        yield self.sender.sendmail(input_mail)

        for recipient in flatten([input_mail.to, input_mail.cc, input_mail.bcc]):
            verify(OutgoingMail).send_message(MailToSmtpFormatCapture(recipient, bccs), TwistedSmtpUserCapture(recipient))


    @defer.inlineCallbacks
    def test_if_recipent_doubled_in_fields_send_only_in_bcc(self):
        input_mail = InputMail.from_dict(duplicates_in_fields_mail_dict(), from_address='pixelated@org')
        when(OutgoingMail).send_message(any(), any()).thenReturn(defer.succeed(None))

        yield self.sender.sendmail(input_mail)

        self.assertIn('to@pixelated.org', input_mail.to)
        self.assertNotIn('another@pixelated.org', input_mail.to)
        #self.assertIn('another@pixelated.org', input_mail.bcc)

    @defer.inlineCallbacks
    def test_if_recipent_doubled_in_fields_send_only_in_to(self):
        input_mail = InputMail.from_dict(duplicates_in_fields_mail_dict(), from_address='pixelated@org')
        when(OutgoingMail).send_message(any(), any()).thenReturn(defer.succeed(None))

        yield self.sender.sendmail(input_mail)

        self.assertIn('third@pixelated.org', input_mail.to)
        self.assertNotIn('third@pixelated.org', input_mail.cc)
        self.assertIn('cc@pixelated.org', input_mail.cc)
        self.assertNotIn(['third@pixelated.org', 'another@pixelated.org'], input_mail.cc)

    def test_remove_canonical_recipient_when_it_is_not_canonical(self):
        recipient = u'user@pixelated.org'

        non_canonical = self.sender._remove_canonical_recipient(recipient)

        self.assertEqual(recipient, non_canonical)

    def test_remove_canonical_recipient_when_it_is_canonical(self):
        recipient = u'User <user@pixelated.org>'

        non_canonical = self.sender._remove_canonical_recipient(recipient)

        self.assertEqual(u'user@pixelated.org', non_canonical)
