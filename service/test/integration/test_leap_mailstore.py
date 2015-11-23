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
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from test.support.integration import SoledadTestBase, load_mail_from_file
from twisted.internet import defer
from pixelated.adapter.model.mail import InputMail


class LeapMailStoreTest(SoledadTestBase):

    @defer.inlineCallbacks
    def setUp(self):
        yield super(LeapMailStoreTest, self).setUp()

    @defer.inlineCallbacks
    def test_get_mail_with_body(self):
        self.maxDiff = None
        mail = load_mail_from_file('mbox00000000')
        mail_id = yield self._create_mail_in_soledad(mail)
        expected_mail_dict = {'body': u'Dignissimos ducimus veritatis. Est tenetur consequatur quia occaecati. Vel sit sit voluptas.\n\nEarum distinctio eos. Accusantium qui sint ut quia assumenda. Facere dignissimos inventore autem sit amet. Pariatur voluptatem sint est.\n\nUt recusandae praesentium aspernatur. Exercitationem amet placeat deserunt quae consequatur eum. Unde doloremque suscipit quia.\n\n', 'header': {u'date': u'Tue, 21 Apr 2015 08:43:27 +0000 (UTC)', u'to': [u'carmel@murazikortiz.name'], u'x-tw-pixelated-tags': u'nite, macro, trash', u'from': u'darby.senger@zemlak.biz', u'subject': u'Itaque consequatur repellendus provident sunt quia.'}, 'ident': mail_id, 'status': [], 'tags': set([]), 'replying': {'all': {'cc-field': [], 'to-field': [u'carmel@murazikortiz.name', u'darby.senger@zemlak.biz']}, 'single': u'darby.senger@zemlak.biz'}, 'textPlainBody': u'Dignissimos ducimus veritatis. Est tenetur consequatur quia occaecati. Vel sit sit voluptas.\n\nEarum distinctio eos. Accusantium qui sint ut quia assumenda. Facere dignissimos inventore autem sit amet. Pariatur voluptatem sint est.\n\nUt recusandae praesentium aspernatur. Exercitationem amet placeat deserunt quae consequatur eum. Unde doloremque suscipit quia.\n\n', 'mailbox': u'inbox', 'attachments': [], 'security_casing': {'imprints': [{'state': 'no_signature_information'}], 'locks': []}}

        result = yield self.mail_store.get_mail(mail_id, include_body=True)
        self.assertIsNotNone(result)
        self.assertEqual(expected_mail_dict, result.as_dict())

    @defer.inlineCallbacks
    def test_round_trip_through_soledad_does_not_modify_content(self):
        mail = load_mail_from_file('mbox00000000')
        mail_id = yield self._create_mail_in_soledad(mail)
        expected_mail_dict = {'body': u'Dignissimos ducimus veritatis. Est tenetur consequatur quia occaecati. Vel sit sit voluptas.\n\nEarum distinctio eos. Accusantium qui sint ut quia assumenda. Facere dignissimos inventore autem sit amet. Pariatur voluptatem sint est.\n\nUt recusandae praesentium aspernatur. Exercitationem amet placeat deserunt quae consequatur eum. Unde doloremque suscipit quia.\n\n', 'header': {u'date': u'Tue, 21 Apr 2015 08:43:27 +0000 (UTC)', u'to': [u'carmel@murazikortiz.name'], u'x-tw-pixelated-tags': u'nite, macro, trash', u'from': u'darby.senger@zemlak.biz', u'subject': u'Itaque consequatur repellendus provident sunt quia.'}, 'ident': mail_id, 'status': [], 'tags': set([])}

        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())
        fetched_mail = yield self.mail_store.get_mail(mail_id, include_body=True)
        self.assertEqual(expected_mail_dict['header'], mail.as_dict()['header'])
        self.assertEqual(expected_mail_dict['header'], fetched_mail.as_dict()['header'])

    @defer.inlineCallbacks
    def test_round_trip_through_soledad_keeps_attachment(self):
        input_mail = MIMEMultipart()
        input_mail.attach(MIMEText(u'a utf8 message', _charset='utf-8'))
        attachment = MIMEApplication('pretend to be binary attachment data')
        attachment.add_header('Content-Disposition', 'attachment', filename='filename.txt')
        input_mail.attach(attachment)

        mail = yield self.mail_store.add_mail('INBOX', input_mail.as_string())
        fetched_mail = yield self.mail_store.get_mail(mail.ident, include_body=True)

        # _, docs = yield self.soledad.get_all_docs()
        # for doc in docs:
        #     print '\n%s\n' % doc

        # self.assertEqual(1, len(mail.as_dict()['attachments']))
        # print fetched_mail.as_dict()
        # self.assertEqual(1, len(fetched_mail.as_dict()['attachments']))

    @defer.inlineCallbacks
    def test_all_mails(self):
        mail = load_mail_from_file('mbox00000000')
        yield self._create_mail_in_soledad(mail)

        mails = yield self.mail_store.all_mails()

        self.assertEqual(1, len(mails))
        self.assertEqual('Itaque consequatur repellendus provident sunt quia.', mails[0].subject)

    @defer.inlineCallbacks
    def test_add_and_remove_mail(self):
        yield self.adaptor.initialize_store(self.soledad)
        mail = load_mail_from_file('mbox00000000')
        yield self.mail_store.add_mailbox('INBOX')

        msg = yield self.mail_store.add_mail('INBOX', mail.as_string())

        yield self.mail_store.delete_mail(msg.mail_id)

        deleted_msg = yield self.mail_store.get_mail(msg.mail_id)

        self.assertIsNone(deleted_msg)

    @defer.inlineCallbacks
    def test_add_add_mail_twice(self):
        yield self.adaptor.initialize_store(self.soledad)
        mail = load_mail_from_file('mbox00000000', enforceUniqueMessageId=True)
        mail2 = load_mail_from_file('mbox00000000', enforceUniqueMessageId=True)
        yield self.mail_store.add_mailbox('INBOX')

        msg1 = yield self.mail_store.add_mail('INBOX', mail.as_string())
        msg2 = yield self.mail_store.add_mail('INBOX', mail2.as_string())

        self.assertIsNotNone(msg1.ident)
        self.assertIsNotNone(msg2.ident)

    @defer.inlineCallbacks
    def test_get_mailbox_mail_ids(self):
        mail = load_mail_from_file('mbox00000000')
        yield self.mail_store.add_mailbox('INBOX')
        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())

        mails = yield self.mail_store.get_mailbox_mail_ids('INBOX')

        self.assertEqual(1, len(mails))
        self.assertEqual(mail.mail_id, mails[0])

    @defer.inlineCallbacks
    def test_get_replying_when_sender_is_not_me(self):
        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'
        mail = load_mail_from_file('mbox00000000')
        del mail['From']
        del mail['To']
        del mail['Cc']
        mail['From'] = 'not-me@pixelated.org'
        mail['To'] = 'addr1@pixelated.org, addr2@pixelated.org'

        yield self.mail_store.add_mailbox('INBOX')
        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())

        replying = mail.as_dict()['replying']

        self.assertEqual(replying['single'], 'not-me@pixelated.org')
        self.assertEqual(replying['all']['to-field'], [u'addr1@pixelated.org', u'addr2@pixelated.org', u'not-me@pixelated.org'])
        self.assertListEqual(replying['all']['cc-field'], [])

    @defer.inlineCallbacks
    def test_get_replying_when_sender_is_me(self):
        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'
        mail = load_mail_from_file('mbox00000000')
        del mail['From']
        del mail['To']
        del mail['Cc']
        mail['From'] = 'me@pixelated.org'
        mail['To'] = 'addr1@pixelated.org, addr2@pixelated.org'

        yield self.mail_store.add_mailbox('INBOX')
        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())

        replying = mail.as_dict()['replying']

        self.assertEqual(replying['single'], 'me@pixelated.org')
        self.assertEqual(replying['all']['to-field'], [u'addr1@pixelated.org', u'addr2@pixelated.org'])
        self.assertEqual(replying['all']['cc-field'], [])

    @defer.inlineCallbacks
    def test_get_replying_when_sender_is_me_to_me(self):
        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'
        mail = load_mail_from_file('mbox00000000')
        del mail['From']
        del mail['To']
        del mail['Cc']
        mail['From'] = 'me@pixelated.org'
        mail['To'] = 'me@pixelated.org'

        yield self.mail_store.add_mailbox('INBOX')
        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())

        replying = mail.as_dict()['replying']

        self.assertEqual(replying['single'], 'me@pixelated.org')
        self.assertEqual(replying['all']['to-field'], [u'me@pixelated.org'])
        self.assertEqual(replying['all']['cc-field'], [])

    @defer.inlineCallbacks
    def test_get_replying_when_sender_is_me_to_recipients_including_me(self):
        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'
        mail = load_mail_from_file('mbox00000000')
        del mail['From']
        del mail['To']
        del mail['Cc']
        mail['From'] = 'me@pixelated.org'
        mail['To'] = 'addr1@pixelated.org, me@pixelated.org'

        yield self.mail_store.add_mailbox('INBOX')
        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())
        replying = mail.as_dict()['replying']

        self.assertEqual(replying['single'], 'me@pixelated.org')
        self.assertEqual(replying['all']['to-field'], [u'addr1@pixelated.org', u'me@pixelated.org'])
        self.assertEqual(replying['all']['cc-field'], [])

    @defer.inlineCallbacks
    def test_deleting_a_deleted_mail_doesnt_raise_errors(self):
        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'
        mail = load_mail_from_file('mbox00000000')
        yield self.mail_store.add_mailbox('INBOX')
        mail = yield self.mail_store.add_mail('INBOX', mail.as_string())

        yield self.mail_store.delete_mail(mail.ident)
        yield self.mail_store.delete_mail(mail.ident)
