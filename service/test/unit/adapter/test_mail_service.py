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
from pixelated.adapter.mailstore.leap_mailstore import LeapMail
from pixelated.adapter.model.mail import InputMail, PixelatedMail

from pixelated.adapter.services.mail_service import MailService
from test.support.test_helper import mail_dict, leap_mail
from mockito import mock, unstub, when, verify, verifyNoMoreInteractions, any
from twisted.internet import defer


class TestMailService(unittest.TestCase):
    def setUp(self):
        self.drafts = mock()
        self.querier = mock()
        self.mail_store = mock()
        self.mailboxes = mock()

        self.mailboxes.drafts = defer.succeed(self.drafts)

        self.mailboxes.trash = mock()
        self.mailboxes.sent = mock()

        self.mail_sender = mock()
        self.search_engine = mock()
        self.mail_service = MailService(self.mailboxes, self.mail_sender, self.mail_store, self.querier, self.search_engine)

    def tearDown(self):
        unstub()

    def test_send_mail(self):
        when(InputMail).from_dict(any()).thenReturn('inputmail')
        when(self.mail_sender).sendmail(any()).thenReturn(defer.Deferred())

        sent_deferred = self.mail_service.send_mail(mail_dict())

        verify(self.mail_sender).sendmail("inputmail")

        sent_deferred.callback('Assume sending mail succeeded')

        return sent_deferred

    @defer.inlineCallbacks
    def test_send_mail_removes_draft(self):
        when(InputMail).from_dict(any()).thenReturn('inputmail')

        deferred_success = defer.succeed(None)
        when(self.mail_sender).sendmail(any()).thenReturn(deferred_success)

        yield self.mail_service.send_mail({'ident': '12'})

        verify(self.mail_sender).sendmail("inputmail")
        verify(self.drafts).remove(any())

    @defer.inlineCallbacks
    def test_send_mail_does_not_delete_draft_on_error(self):
        when(InputMail).from_dict(any()).thenReturn('inputmail')

        deferred_failure = defer.fail(Exception("Assume sending mail failed"))
        when(self.mail_sender).sendmail(any()).thenReturn(deferred_failure)

        try:
            yield self.mail_service.send_mail({'ident': '12'})
            self.fail("send_mail is expected to raise if underlying call fails")
        except:
            verify(self.mail_sender).sendmail("inputmail")
            verifyNoMoreInteractions(self.drafts)

    def test_mark_as_read(self):
        mail = mock()
        when(self.mail_service).mail(any()).thenReturn(mail)
        self.mail_service.mark_as_read(1)

        verify(mail).mark_as_read()

    def test_delete_mail(self):
        mail_to_delete = LeapMail(1, 'INBOX')
        when(self.mail_store).get_mail(1).thenReturn(mail_to_delete)

        self.mail_service.delete_mail(1)

        verify(self.mail_store).move_mail_to_mailbox(1, 'TRASH')

    def test_recover_mail(self):
        mail_to_recover = PixelatedMail.from_soledad(*leap_mail(), soledad_querier=None)
        when(self.mail_service).mail(1).thenReturn(mail_to_recover)
        when(self.mailboxes).move_to_inbox(1).thenReturn(mail_to_recover)

        self.mail_service.recover_mail(1)

        verify(self.mailboxes).move_to_inbox(1)
        verify(self.search_engine).index_mail(mail_to_recover)
