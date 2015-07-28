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
from email.parser import Parser
from leap.mail.mail import Message
import pkg_resources
import os
from pixelated.adapter.mailstore.leap_mailstore import LeapMailStore
from test.support.integration import SoledadTestBase
from leap.mail.adaptors.soledad import SoledadMailAdaptor
from twisted.internet import defer
from uuid import uuid4


class LeapMailStoreTest(SoledadTestBase):

    @defer.inlineCallbacks
    def setUp(self):
        yield super(LeapMailStoreTest, self).setUp()
        self.adaptor = SoledadMailAdaptor()
        self.mbox_uuid = str(uuid4())
        self.store = LeapMailStore(self.soledad)

    @defer.inlineCallbacks
    def test_get_mail_with_body(self):
        mail = _load_mail_from_file('mbox00000000')
        mail_id = yield self._create_mail_in_soledad(mail)
        expected_mail_dict = {'body': u'Dignissimos ducimus veritatis. Est tenetur consequatur quia occaecati. Vel sit sit voluptas.\n\nEarum distinctio eos. Accusantium qui sint ut quia assumenda. Facere dignissimos inventore autem sit amet. Pariatur voluptatem sint est.\n\nUt recusandae praesentium aspernatur. Exercitationem amet placeat deserunt quae consequatur eum. Unde doloremque suscipit quia.\n\n', 'header': {u'date': u'Tue, 21 Apr 2015 08:43:27 +0000 (UTC)', u'to': u'carmel@murazikortiz.name', u'x-tw-pixelated-tags': u'nite, macro, trash', u'from': u'darby.senger@zemlak.biz', u'subject': u'Itaque consequatur repellendus provident sunt quia.'}, 'ident': mail_id, 'tags': set([])}

        result = yield self.store.get_mail(mail_id, include_body=True)
        self.assertIsNotNone(result)
        self.assertEqual(expected_mail_dict, result.as_dict())

    @defer.inlineCallbacks
    def test_all_mails(self):
        mail = _load_mail_from_file('mbox00000000')
        yield self._create_mail_in_soledad(mail)

        mails = yield self.store.all_mails()

        self.assertEqual(1, len(mails))
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mails[0].subject)

    @defer.inlineCallbacks
    def test_add_and_remove_mail(self):
        yield self.adaptor.initialize_store(self.soledad)
        mail = _load_mail_from_file('mbox00000000')
        yield self.store.add_mailbox('INBOX')

        msg = yield self.store.add_mail('INBOX', mail.as_string())

        yield self.store.delete_mail(msg.mail_id)

        deleted_msg = yield self.store.get_mail(msg.mail_id)

        self.assertIsNone(deleted_msg)

    @defer.inlineCallbacks
    def test_get_mailbox_mail_ids(self):
        mail = _load_mail_from_file('mbox00000000')
        yield self.store.add_mailbox('INBOX')
        mail = yield self.store.add_mail('INBOX', mail.as_string())

        mails = yield self.store.get_mailbox_mail_ids('INBOX')

        self.assertEqual(1, len(mails))
        self.assertEqual(mail.mail_id, mails[0])

    @defer.inlineCallbacks
    def _create_mail_in_soledad(self, mail):
        message = self._convert_mail_to_leap_message(mail)
        yield self.adaptor.initialize_store(self.soledad)
        yield self.adaptor.create_msg(self.soledad, message)

        defer.returnValue(message.get_wrapper().mdoc.doc_id)

    def _convert_mail_to_leap_message(self, mail):
        message = self.adaptor.get_msg_from_string(Message, mail.as_string())
        message.get_wrapper().set_mbox_uuid(self.mbox_uuid)
        return message


def _load_mail_from_file(mail_file):
    mailset_dir = pkg_resources.resource_filename('test.unit.fixtures', 'mailset')
    mail_file = os.path.join(mailset_dir, 'new', mail_file)
    with open(mail_file) as f:
        mail = Parser().parse(f)
    return mail
