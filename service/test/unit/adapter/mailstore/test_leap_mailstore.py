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
from twisted.trial.unittest import TestCase

from leap.mail import constants
from leap.mail.imap.account import IMAPAccount
from twisted.internet import defer

from mockito import mock, when, any, unstub
from uuid import uuid4
from pixelated.adapter.mailstore.leap_mailstore import LeapMailStore, LeapMail
from leap.mail.adaptors.soledad import SoledadMailAdaptor
import pkg_resources
from email.parser import Parser
import os
from leap.mail.mail import Message


class TestLeapMailStore(TestCase):
    def setUp(self):
        self.account = mock(mocked_obj=IMAPAccount)
        self.soledad = mock()

    @defer.inlineCallbacks
    def test_get_mail_not_exist(self):
        store = LeapMailStore(self.account, self.soledad)

        mail = yield store.get_mail(_format_mdoc_id(uuid4(), 1))

        self.assertIsNone(mail)

    @defer.inlineCallbacks
    def test_get_mail(self):
        mbox_uuid = str(uuid4())

        mdoc_id = self._add_mail_fixture_to_soledad(mbox_uuid)

        store = LeapMailStore(self.account, self.soledad)

        mail = yield store.get_mail(mdoc_id)

        self.assertIsInstance(mail, LeapMail)
        self.assertEqual('darby.senger@zemlak.biz', mail.from_sender)
        self.assertEqual('carmel@murazikortiz.name', mail.to)
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mail.subject)
        self.assertIsNone(mail.body)

    def _add_mail_fixture_to_soledad(self, mbox_uuid, mail_file='mbox00000000'):
        mail = self._load_mail_from_file(mail_file)

        msg = SoledadMailAdaptor().get_msg_from_string(Message, mail.as_string())

        msg.get_wrapper().mdoc.set_mbox_uuid(mbox_uuid)

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