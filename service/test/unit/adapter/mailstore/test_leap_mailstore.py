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
from uuid import uuid4
from email.parser import Parser
import os

from twisted.internet.defer import FirstError
from twisted.trial.unittest import TestCase
from leap.mail import constants
from leap.mail.imap.account import IMAPAccount
from twisted.internet import defer
from mockito import mock, when
from leap.mail.adaptors.soledad import SoledadMailAdaptor
import pkg_resources
from leap.mail.mail import Message

from pixelated.adapter.mailstore.leap_mailstore import LeapMailStore, LeapMail


class TestLeapMail(TestCase):
    def test_leap_mail(self):
        mail = LeapMail('', {'From': 'test@example.test', 'Subject': 'A test Mail', 'To': 'receiver@example.test'})

        self.assertEqual('test@example.test', mail.from_sender)
        self.assertEqual('receiver@example.test', mail.to)
        self.assertEqual('A test Mail', mail.subject)

    def test_as_dict(self):
        mail = LeapMail('doc id', {'From': 'test@example.test', 'Subject': 'A test Mail', 'To': 'receiver@example.test'}, ('foo', 'bar'))

        expected = {
            'header': {
                'from': 'test@example.test',
                'subject': 'A test Mail',
                'to': 'receiver@example.test',

            },
            'ident': 'doc id',
            'tags': ('foo', 'bar'),
        }

        self.assertEqual(expected, mail.as_dict())


class TestLeapMailStore(TestCase):
    def setUp(self):
        self.account = mock(mocked_obj=IMAPAccount)
        self.soledad = mock()
        self.mbox_uuid = str(uuid4())

    @defer.inlineCallbacks
    def test_get_mail_not_exist(self):
        store = LeapMailStore(self.account, self.soledad)

        mail = yield store.get_mail(_format_mdoc_id(uuid4(), 1))

        self.assertIsNone(mail)

    @defer.inlineCallbacks
    def test_get_mail(self):
        mdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')

        store = LeapMailStore(self.account, self.soledad)

        mail = yield store.get_mail(mdoc_id)

        self.assertIsInstance(mail, LeapMail)
        self.assertEqual('darby.senger@zemlak.biz', mail.from_sender)
        self.assertEqual('carmel@murazikortiz.name', mail.to)
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mail.subject)
        self.assertIsNone(mail.body)

    @defer.inlineCallbacks
    def test_get_two_different_mails(self):
        first_mdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')
        second_mdoc_id = self._add_mail_fixture_to_soledad('mbox00000001')

        store = LeapMailStore(self.account, self.soledad)

        mail1 = yield store.get_mail(first_mdoc_id)
        mail2 = yield store.get_mail(second_mdoc_id)

        self.assertNotEqual(mail1, mail2)
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mail1.subject)
        self.assertEqual('Error illum dignissimos autem eos aspernatur.', mail2.subject)

    @defer.inlineCallbacks
    def test_get_mails(self):
        first_mdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')
        second_mdoc_id = self._add_mail_fixture_to_soledad('mbox00000001')

        store = LeapMailStore(self.account, self.soledad)

        mails = yield store.get_mails([first_mdoc_id,second_mdoc_id])

        self.assertEqual(2, len(mails))
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mails[0].subject)
        self.assertEqual('Error illum dignissimos autem eos aspernatur.', mails[1].subject)

    @defer.inlineCallbacks
    def test_get_mails_fails_for_invalid_mail_id(self):
        store = LeapMailStore(self.account, self.soledad)

        try:
            yield store.get_mails(['invalid'])
            self.fail('Exception expected')
        except FirstError:
            pass

    def _add_mail_fixture_to_soledad(self, mail_file):
        mail = self._load_mail_from_file(mail_file)

        msg = SoledadMailAdaptor().get_msg_from_string(Message, mail.as_string())

        msg.get_wrapper().mdoc.set_mbox_uuid(self.mbox_uuid)

        mdoc_id = msg.get_wrapper().mdoc.future_doc_id
        fdoc_id = msg.get_wrapper().mdoc.fdoc
        hdoc_id = msg.get_wrapper().mdoc.hdoc
        cdoc_id = msg.get_wrapper().mdoc.cdocs[0]

        when(self.soledad).get_doc(mdoc_id).thenReturn(defer.succeed(msg.get_wrapper().mdoc.serialize()))
        when(self.soledad).get_doc(fdoc_id).thenReturn(defer.succeed(msg.get_wrapper().fdoc.serialize()))
        when(self.soledad).get_doc(hdoc_id).thenReturn(defer.succeed(msg.get_wrapper().hdoc.serialize()))
        when(self.soledad).get_doc(cdoc_id).thenReturn(defer.succeed(msg.get_wrapper().cdocs[1].serialize()))

        return mdoc_id

    def _load_mail_from_file(self, mail_file):
        mailset_dir = pkg_resources.resource_filename('test.unit.fixtures', 'mailset')
        mail_file = os.path.join(mailset_dir, 'new', mail_file)
        with open(mail_file) as f:
            mail = Parser().parse(f)
        return mail


def _format_mdoc_id(mbox_uuid, chash):
    return constants.METAMSGID.format(mbox_uuid=mbox_uuid, chash=chash)