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
import json
from uuid import uuid4
from email.parser import Parser
import os
from leap.soledad.common.document import SoledadDocument
from leap.mail.adaptors.soledad_indexes import MAIL_INDEXES
from twisted.internet.defer import FirstError
from twisted.trial.unittest import TestCase
from leap.mail import constants
from twisted.internet import defer
from mockito import mock, when, verify, any
import test.support.mockito
from leap.mail.adaptors.soledad import SoledadMailAdaptor, MailboxWrapper
import pkg_resources
from leap.mail.mail import Message
from pixelated.adapter.mailstore import underscore_uuid

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
            'body': None
        }

        self.assertEqual(expected, mail.as_dict())

    def test_as_dict_with_body(self):
        body = 'some body content'
        mail = LeapMail('doc id', {'From': 'test@example.test', 'Subject': 'A test Mail', 'To': 'receiver@example.test'}, ('foo', 'bar'), body=body)

        self.assertEqual(body, mail.as_dict()['body'])


class TestLeapMailStore(TestCase):
    def setUp(self):
        self.soledad = mock()
        self.mbox_uuid = str(uuid4())
        self.doc_by_id = {}
        self.mbox_uuid_by_name = {}

    @defer.inlineCallbacks
    def test_get_mail_not_exist(self):
        store = LeapMailStore(self.soledad)

        mail = yield store.get_mail(_format_mdoc_id(uuid4(), 1))

        self.assertIsNone(mail)

    @defer.inlineCallbacks
    def test_get_mail(self):
        mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000000')

        store = LeapMailStore(self.soledad)

        mail = yield store.get_mail(mdoc_id)

        self.assertIsInstance(mail, LeapMail)
        self.assertEqual('darby.senger@zemlak.biz', mail.from_sender)
        self.assertEqual('carmel@murazikortiz.name', mail.to)
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mail.subject)
        self.assertIsNone(mail.body)

    @defer.inlineCallbacks
    def test_get_two_different_mails(self):
        first_mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000000')
        second_mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000001')

        store = LeapMailStore(self.soledad)

        mail1 = yield store.get_mail(first_mdoc_id)
        mail2 = yield store.get_mail(second_mdoc_id)

        self.assertNotEqual(mail1, mail2)
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mail1.subject)
        self.assertEqual('Error illum dignissimos autem eos aspernatur.', mail2.subject)

    @defer.inlineCallbacks
    def test_get_mails(self):
        first_mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000000')
        second_mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000001')

        store = LeapMailStore(self.soledad)

        mails = yield store.get_mails([first_mdoc_id, second_mdoc_id])

        self.assertEqual(2, len(mails))
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mails[0].subject)
        self.assertEqual('Error illum dignissimos autem eos aspernatur.', mails[1].subject)

    @defer.inlineCallbacks
    def test_get_mails_fails_for_invalid_mail_id(self):
        store = LeapMailStore(self.soledad)

        try:
            yield store.get_mails(['invalid'])
            self.fail('Exception expected')
        except FirstError:
            pass

    @defer.inlineCallbacks
    def test_get_mail_with_body(self):
        expeted_body = 'Dignissimos ducimus veritatis. Est tenetur consequatur quia occaecati. Vel sit sit voluptas.\n\nEarum distinctio eos. Accusantium qui sint ut quia assumenda. Facere dignissimos inventore autem sit amet. Pariatur voluptatem sint est.\n\nUt recusandae praesentium aspernatur. Exercitationem amet placeat deserunt quae consequatur eum. Unde doloremque suscipit quia.\n\n'
        mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000000')

        store = LeapMailStore(self.soledad)

        mail = yield store.get_mail(mdoc_id, include_body=True)

        self.assertEqual(expeted_body, mail.body)

    @defer.inlineCallbacks
    def test_update_mail(self):
        mdoc_id, fdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')
        soledad_fdoc = self.doc_by_id[fdoc_id]
        when(self.soledad).put_doc(soledad_fdoc).thenReturn(defer.succeed(None))

        store = LeapMailStore(self.soledad)

        mail = yield store.get_mail(mdoc_id)

        mail.tags.add('new_tag')

        yield store.update_mail(mail)

        verify(self.soledad).put_doc(soledad_fdoc)
        self.assertTrue('new_tag' in soledad_fdoc.content['tags'])

    @defer.inlineCallbacks
    def test_all_mails(self):
        first_mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000000')
        second_mdoc_id, _ = self._add_mail_fixture_to_soledad('mbox00000001')
        when(self.soledad).get_from_index('by-type', 'meta').thenReturn(defer.succeed([self.doc_by_id[first_mdoc_id], self.doc_by_id[second_mdoc_id]]))

        store = LeapMailStore(self.soledad)

        mails = yield store.all_mails()

        self.assertIsNotNone(mails)
        self.assertEqual(2, len(mails))
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mails[0].subject)
        self.assertEqual('Error illum dignissimos autem eos aspernatur.', mails[1].subject)

    @defer.inlineCallbacks
    def test_add_mailbox(self):
        when(self.soledad).list_indexes().thenReturn(defer.succeed(MAIL_INDEXES)).thenReturn(defer.succeed(MAIL_INDEXES))
        when(self.soledad).get_from_index('by-type-and-mbox', 'mbox', 'TEST').thenReturn(defer.succeed([]))
        when(self.soledad).create_doc(any()).thenReturn(defer.succeed(None))
        self._mock_create_doc(self.mbox_uuid, MailboxWrapper(mbox='TEST'))
        store = LeapMailStore(self.soledad)

        mbox = yield store.add_mailbox('TEST')

        self.assertIsNotNone(mbox)
        self.assertEqual(self.mbox_uuid, mbox.doc_id)
        self.assertEqual('TEST', mbox.mbox)
        # assert index got updated

    @defer.inlineCallbacks
    def test_add_mail(self):
        expected_message = self._add_create_mail_mocks_to_soledad('mbox00000000')
        mail = self._load_mail_from_file('mbox00000000')
        self._mock_get_mailbox('INBOX')

        store = LeapMailStore(self.soledad)

        message = yield store.add_mail('INBOX', mail.as_string())

        self.assertIsInstance(message, LeapMail)
        self._assert_message_docs_created(expected_message, message)

    @defer.inlineCallbacks
    def test_delete_mail(self):
        mdoc_id, fdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')

        store = LeapMailStore(self.soledad)

        yield store.delete_mail(mdoc_id)

        verify(self.soledad).delete_doc(self.doc_by_id[mdoc_id])
        verify(self.soledad).delete_doc(self.doc_by_id[fdoc_id])

    @defer.inlineCallbacks
    def test_get_mailbox_mail_ids(self):
        mdoc_id, fdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')
        when(self.soledad).get_from_index('by-type-and-mbox-uuid', 'flags', underscore_uuid(self.mbox_uuid)).thenReturn(defer.succeed([self.doc_by_id[fdoc_id]]))
        self._mock_get_mailbox('INBOX')
        store = LeapMailStore(self.soledad)

        mail_ids = yield store.get_mailbox_mail_ids('INBOX')

        self.assertEqual(1, len(mail_ids))
        self.assertEqual(mdoc_id, mail_ids[0])

    @defer.inlineCallbacks
    def test_delete_mailbox(self):
        _, mbox_soledad_doc = self._mock_get_mailbox('INBOX')
        store = LeapMailStore(self.soledad)
        when(self.soledad).delete_doc(mbox_soledad_doc).thenReturn(defer.succeed(None))

        yield store.delete_mailbox('INBOX')

        verify(self.soledad).delete_doc(self.doc_by_id[mbox_soledad_doc.doc_id])
        # should also verify index is updated

    @defer.inlineCallbacks
    def test_copy_mail_to_mailbox(self):
        expected_message = self._add_create_mail_mocks_to_soledad('mbox00000000')
        mail_id, fdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')
        self._mock_get_mailbox('TRASH')
        store = LeapMailStore(self.soledad)

        mail = yield store.copy_mail_to_mailbox(mail_id, 'TRASH')

        self._assert_message_docs_created(expected_message, mail, only_mdoc_and_fdoc=True)

    @defer.inlineCallbacks
    def test_move_to_mailbox(self):
        expected_message = self._add_create_mail_mocks_to_soledad('mbox00000000')
        mail_id, fdoc_id = self._add_mail_fixture_to_soledad('mbox00000000')
        self._mock_get_mailbox('TRASH')
        store = LeapMailStore(self.soledad)

        mail = yield store.move_mail_to_mailbox(mail_id, 'TRASH')

        self._assert_message_docs_created(expected_message, mail, only_mdoc_and_fdoc=True)
        # verify(self.soledad).delete_doc(self.doc_by_id[mail_id])
        # verify(self.soledad).delete_doc(self.doc_by_id[fdoc_id])

    def _assert_message_docs_created(self, expected_message, actual_message, only_mdoc_and_fdoc=False):
        wrapper = expected_message.get_wrapper()

        verify(self.soledad).create_doc(wrapper.mdoc.serialize(), doc_id=actual_message.mail_id)
        verify(self.soledad).create_doc(wrapper.fdoc.serialize(), doc_id=wrapper.fdoc.future_doc_id)
        if not only_mdoc_and_fdoc:
            verify(self.soledad).create_doc(wrapper.hdoc.serialize(), doc_id=wrapper.hdoc.future_doc_id)
            for nr, cdoc in wrapper.cdocs.items():
                verify(self.soledad).create_doc(cdoc.serialize(), doc_id=wrapper.cdocs[nr].future_doc_id)

    def _mock_get_mailbox(self, mailbox_name, create_new_uuid=False):
        mbox_uuid = self.mbox_uuid if not create_new_uuid else str(uuid4())
        when(self.soledad).list_indexes().thenReturn(defer.succeed(MAIL_INDEXES)).thenReturn(
            defer.succeed(MAIL_INDEXES))
        mbox = MailboxWrapper(doc_id=mbox_uuid, mbox=mailbox_name, uuid=mbox_uuid)
        soledad_doc = SoledadDocument(mbox_uuid, json=json.dumps(mbox.serialize()))
        when(self.soledad).get_from_index('by-type-and-mbox', 'mbox', mailbox_name).thenReturn(defer.succeed([soledad_doc]))
        self._mock_soledad_doc(mbox_uuid, mbox)

        self.mbox_uuid_by_name[mailbox_name] = mbox_uuid

        return mbox, soledad_doc

    def _add_mail_fixture_to_soledad(self, mail_file):
        mail = self._load_mail_from_file(mail_file)
        msg = self._convert_mail_to_leap_message(mail)
        wrapper = msg.get_wrapper()

        mdoc_id = wrapper.mdoc.future_doc_id
        fdoc_id = wrapper.mdoc.fdoc
        hdoc_id = wrapper.mdoc.hdoc
        cdoc_id = wrapper.mdoc.cdocs[0]

        self._mock_soledad_doc(mdoc_id, wrapper.mdoc)
        self._mock_soledad_doc(fdoc_id, wrapper.fdoc)
        self._mock_soledad_doc(hdoc_id, wrapper.hdoc)
        self._mock_soledad_doc(cdoc_id, wrapper.cdocs[1])

        return mdoc_id, fdoc_id

    def _add_create_mail_mocks_to_soledad(self, mail_file):
        mail = self._load_mail_from_file(mail_file)
        msg = self._convert_mail_to_leap_message(mail)
        wrapper = msg.get_wrapper()

        mdoc_id = wrapper.mdoc.future_doc_id
        fdoc_id = wrapper.mdoc.fdoc
        hdoc_id = wrapper.mdoc.hdoc
        cdoc_id = wrapper.mdoc.cdocs[0]

        self._mock_create_doc(mdoc_id, wrapper.mdoc)
        self._mock_create_doc(fdoc_id, wrapper.fdoc)
        self._mock_create_doc(hdoc_id, wrapper.hdoc)
        self._mock_create_doc(cdoc_id, wrapper.cdocs[1])

        return msg

    def _convert_mail_to_leap_message(self, mail):
        msg = SoledadMailAdaptor().get_msg_from_string(Message, mail.as_string())
        msg.get_wrapper().set_mbox_uuid(self.mbox_uuid)
        return msg

    def _mock_soledad_doc(self, doc_id, doc):
        soledad_doc = SoledadDocument(doc_id, json=json.dumps(doc.serialize()))

        # when(self.soledad).get_doc(doc_id).thenReturn(defer.succeed(soledad_doc))
        when(self.soledad).get_doc(doc_id).thenAnswer(lambda: defer.succeed(soledad_doc))

        self.doc_by_id[doc_id] = soledad_doc

    def _mock_create_doc(self, doc_id, doc):
        soledad_doc = SoledadDocument(doc_id, json=json.dumps(doc.serialize()))
        if doc.future_doc_id:
            when(self.soledad).create_doc(doc.serialize(), doc_id=doc_id).thenReturn(defer.succeed(soledad_doc))
        else:
            when(self.soledad).create_doc(doc.serialize()).thenReturn(defer.succeed(soledad_doc))
        self.doc_by_id[doc_id] = soledad_doc

    def _load_mail_from_file(self, mail_file):
        mailset_dir = pkg_resources.resource_filename('test.unit.fixtures', 'mailset')
        mail_file = os.path.join(mailset_dir, 'new', mail_file)
        with open(mail_file) as f:
            mail = Parser().parse(f)
        return mail


def _format_mdoc_id(mbox_uuid, chash):
    return constants.METAMSGID.format(mbox_uuid=mbox_uuid, chash=chash)
