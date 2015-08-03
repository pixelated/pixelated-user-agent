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
from test.support.integration import SoledadTestBase, load_mail_from_file
from twisted.internet import defer


class LeapMailStoreTest(SoledadTestBase):

    @defer.inlineCallbacks
    def setUp(self):
        yield super(LeapMailStoreTest, self).setUp()

    @defer.inlineCallbacks
    def test_get_mail_with_body(self):
        mail = load_mail_from_file('mbox00000000')
        mail_id = yield self._create_mail_in_soledad(mail)
        expected_mail_dict = {'body': u'Dignissimos ducimus veritatis. Est tenetur consequatur quia occaecati. Vel sit sit voluptas.\n\nEarum distinctio eos. Accusantium qui sint ut quia assumenda. Facere dignissimos inventore autem sit amet. Pariatur voluptatem sint est.\n\nUt recusandae praesentium aspernatur. Exercitationem amet placeat deserunt quae consequatur eum. Unde doloremque suscipit quia.\n\n', 'header': {u'date': u'Tue, 21 Apr 2015 08:43:27 +0000 (UTC)', u'to': u'carmel@murazikortiz.name', u'x-tw-pixelated-tags': u'nite, macro, trash', u'from': u'darby.senger@zemlak.biz', u'subject': u'Itaque consequatur repellendus provident sunt quia.'}, 'ident': mail_id, 'tags': set([])}

        result = yield self.store.get_mail(mail_id, include_body=True)
        self.assertIsNotNone(result)
        self.assertEqual(expected_mail_dict, result.as_dict())

    @defer.inlineCallbacks
    def test_all_mails(self):
        mail = load_mail_from_file('mbox00000000')
        yield self._create_mail_in_soledad(mail)

        mails = yield self.store.all_mails()

        self.assertEqual(1, len(mails))
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mails[0].subject)

    @defer.inlineCallbacks
    def test_add_and_remove_mail(self):
        yield self.adaptor.initialize_store(self.soledad)
        mail = load_mail_from_file('mbox00000000')
        yield self.store.add_mailbox('INBOX')

        msg = yield self.store.add_mail('INBOX', mail.as_string())

        yield self.store.delete_mail(msg.mail_id)

        deleted_msg = yield self.store.get_mail(msg.mail_id)

        self.assertIsNone(deleted_msg)

    @defer.inlineCallbacks
    def test_get_mailbox_mail_ids(self):
        mail = load_mail_from_file('mbox00000000')
        yield self.store.add_mailbox('INBOX')
        mail = yield self.store.add_mail('INBOX', mail.as_string())

        mails = yield self.store.get_mailbox_mail_ids('INBOX')

        self.assertEqual(1, len(mails))
        self.assertEqual(mail.mail_id, mails[0])

