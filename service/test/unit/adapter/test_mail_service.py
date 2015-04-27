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
from pixelated.adapter.model.mail import InputMail, PixelatedMail

from pixelated.adapter.services.mail_service import MailService
from test.support.test_helper import mail_dict, leap_mail
from mockito import mock, unstub, when, verify, verifyNoMoreInteractions, any
from twisted.internet.defer import Deferred


class TestMailService(unittest.TestCase):
    def setUp(self):
        self.drafts = mock()
        self.querier = mock()
        self.mailboxes = mock()
        self.mailboxes.drafts = lambda: self.drafts
        self.mailboxes.trash = lambda: mock()
        self.mailboxes.sent = lambda: mock()

        self.mail_sender = mock()
        self.search_engine = mock()
        self.mail_service = MailService(self.mailboxes, self.mail_sender, self.querier, self.search_engine)

    def tearDown(self):
        unstub()

    def test_send_mail(self):
        when(InputMail).from_dict(any()).thenReturn('inputmail')
        when(self.mail_sender).sendmail(any()).thenReturn(Deferred())

        sent_deferred = self.mail_service.send_mail(mail_dict())

        verify(self.mail_sender).sendmail("inputmail")

        sent_deferred.callback('Assume sending mail succeeded')

        return sent_deferred

    def test_send_mail_removes_draft(self):
        mail_ident = 'Some ident'
        mail = mail_dict()
        mail['ident'] = mail_ident
        when(InputMail).from_dict(any()).thenReturn('inputmail')
        deferred = Deferred()
        when(self.mail_sender).sendmail(any()).thenReturn(deferred)

        sent_deferred = self.mail_service.send_mail(mail)

        verify(self.mail_sender).sendmail("inputmail")

        def assert_removed_from_drafts(_):
            verify(self.drafts).remove(any())

        sent_deferred.addCallback(assert_removed_from_drafts)
        sent_deferred.callback('Assume sending mail succeeded')

        return sent_deferred

    def test_send_mail_does_not_delete_draft_on_error(self):
        when(InputMail).from_dict(any()).thenReturn('inputmail')
        when(self.mail_sender).sendmail(any()).thenReturn(Deferred())

        send_deferred = self.mail_service.send_mail(mail_dict())

        verify(self.mail_sender).sendmail("inputmail")

        def assert_not_removed_from_drafts(_):
            verifyNoMoreInteractions(self.drafts)

        send_deferred.addErrback(assert_not_removed_from_drafts)

        send_deferred.errback(Exception('Assume sending mail failed'))

        return send_deferred

    def test_mark_as_read(self):
        mail = mock()
        when(self.mail_service).mail(any()).thenReturn(mail)
        self.mail_service.mark_as_read(1)

        verify(mail).mark_as_read()

    def test_delete_mail(self):
        mail_to_delete = PixelatedMail.from_soledad(*leap_mail(), soledad_querier=None)
        when(self.mail_service).mail(1).thenReturn(mail_to_delete)

        self.mail_service.delete_mail(1)

        verify(self.mailboxes).move_to_trash(1)

    def test_recover_mail(self):
        mail_to_recover = PixelatedMail.from_soledad(*leap_mail(), soledad_querier=None)
        when(self.mail_service).mail(1).thenReturn(mail_to_recover)
        when(self.mailboxes).move_to_inbox(1).thenReturn(mail_to_recover)

        self.mail_service.recover_mail(1)

        verify(self.mailboxes).move_to_inbox(1)
        verify(self.search_engine).index_mail(mail_to_recover)
