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
import unittest

import pixelated.support.date
from pixelated.adapter.model.mail import PixelatedMail, InputMail
from mockito import *
from test.support import test_helper
import dateutil.parser as dateparser
import base64
from leap.mail.imap.fields import fields
from datetime import datetime


class TestPixelatedMail(unittest.TestCase):
    def setUp(self):
        self.querier = mock()

    def test_parse_date_from_soledad_uses_date_header_if_available(self):
        leap_mail_date = 'Wed, 3 Sep 2014 12:36:17 -0300'
        leap_mail_date_in_iso_format = "2014-09-03T12:36:17-03:00"

        leap_mail = test_helper.leap_mail(headers={'date': leap_mail_date})

        mail = PixelatedMail.from_soledad(*leap_mail, soledad_querier=self.querier)

        self.assertEqual(str(mail.headers['Date']), leap_mail_date_in_iso_format)

    def test_parse_date_from_soledad_fallback_to_received_header_if_date_header_isnt_available(self):
        leap_mail_date = "Wed, 03 Sep 2014 13:11:15 -0300"
        leap_mail_date_in_iso_format = "2014-09-03T13:11:15-03:00"
        leap_mail_received_header = "by bitmask.local from 127.0.0.1 with ESMTP ;\n " + leap_mail_date

        leap_mail = test_helper.leap_mail(headers={'received': leap_mail_received_header})

        mail = PixelatedMail.from_soledad(*leap_mail, soledad_querier=self.querier)

        self.assertEqual(str(mail.headers['Date']), leap_mail_date_in_iso_format)

    def test_update_tags_return_a_set_with_the_current_tags(self):
        soledad_docs = test_helper.leap_mail(extra_headers={'X-tags': '["custom_1", "custom_2"]'})
        pixelated_mail = PixelatedMail.from_soledad(*soledad_docs, soledad_querier=self.querier)

        current_tags = pixelated_mail.update_tags({'custom_1', 'custom_3'})
        self.assertEquals({'custom_3', 'custom_1'}, current_tags)

    def test_mark_as_read(self):
        mail = PixelatedMail.from_soledad(*test_helper.leap_mail(flags=[]), soledad_querier=self.querier)

        mail.mark_as_read()

        self.assertEquals(mail.fdoc.content['flags'], ['\\Seen'])

    def test_mark_as_not_recent(self):
        mail = PixelatedMail.from_soledad(*test_helper.leap_mail(flags=['\\Recent']), soledad_querier=self.querier)

        mail.mark_as_not_recent()

        self.assertEquals(mail.fdoc.content['flags'], [])

    def test_get_for_save_adds_from(self):
        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'
        headers = {'Subject': 'The subject',
                   'Date': str(datetime.now()),
                   'To': 'me@pixelated.org'}

        input_mail = InputMail()
        input_mail.headers = headers

        self.assertEqual('me@pixelated.org', input_mail.get_for_save(1, 'SENT')[1][fields.HEADERS_KEY]['From'])

    def test_as_dict(self):
        headers = {'Subject': 'The subject',
                   'From': 'someone@pixelated.org',
                   'To': 'me@pixelated.org'}
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'],
                                                 extra_headers=headers)

        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'

        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)

        _dict = mail.as_dict()

        self.maxDiff = None

        self.assertEquals(_dict, {'htmlBody': None,
                                  'textPlainBody': 'body',
                                  'header': {
                                      'date': dateparser.parse(hdoc.content['date']).isoformat(),
                                      'from': 'someone@pixelated.org',
                                      'subject': 'The subject',
                                      'to': ['me@pixelated.org'],
                                      'cc': [],
                                      'bcc': []
                                  },
                                  'ident': 'chash',
                                  'mailbox': 'inbox',
                                  'security_casing': {'imprints': [{'state': 'no_signature_information'}], 'locks': []},
                                  'status': ['recent'],
                                  'tags': [],
                                  'attachments': [],
                                  'replying': {
                                      'single': 'someone@pixelated.org',
                                      'all': {
                                          'to-field': ['someone@pixelated.org'],
                                          'cc-field': []
                                      }
                                  }})

    def test_use_reply_to_address_for_replying(self):
        headers = {'Subject': 'The subject',
                   'From': 'someone@pixelated.org',
                   'Reply-To': 'reply-to-this-address@pixelated.org',
                   'To': 'me@pixelated.org, \nalice@pixelated.org'}
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'],
                                                 extra_headers=headers)

        InputMail.FROM_EMAIL_ADDRESS = 'me@pixelated.org'

        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)

        _dict = mail.as_dict()

        self.assertEquals(_dict['replying'], {'single': 'reply-to-this-address@pixelated.org',
                                              'all': {
                                                  'to-field': ['alice@pixelated.org', 'reply-to-this-address@pixelated.org'],
                                                  'cc-field': []
                                              }})

    def test_alternatives_body(self):
        parts = {'alternatives': [], 'attachments': []}
        parts['alternatives'].append({'content': 'blablabla', 'headers': {'Content-Type': 'text/plain'}})
        parts['alternatives'].append({'content': '<p>blablabla</p>', 'headers': {'Content-Type': 'text/html'}})

        mail = PixelatedMail.from_soledad(None, None, self._create_bdoc(raw='blablabla'), parts=parts, soledad_querier=None)

        self.assertRegexpMatches(mail.html_body, '^<p>blablabla</p>$')
        self.assertRegexpMatches(mail.text_plain_body, '^blablabla$')

    def test_html_is_none_if_multiple_alternatives_have_no_html_part(self):
        parts = {
            'attachments': [],
            'alternatives': [
                {'content': u'content', 'headers': {u'Content-Type': u'text/plain; charset=us-ascii'}},
                {'content': u'', 'headers': {u'Some info': u'info'}}]}

        mail = PixelatedMail.from_soledad(None, None, None, parts=parts, soledad_querier=None)
        self.assertIsNone(mail.html_body)

    def test_percent_character_is_allowed_on_body(self):
        parts = {'alternatives': [], 'attachments': []}
        parts['alternatives'].append({'content': '100% happy with percentage symbol', 'headers': {'Content-Type': 'text/plain'}})
        parts['alternatives'].append({'content': '<p>100% happy with percentage symbol</p>', 'headers': {'Content-Type': 'text/html'}})

        mail = PixelatedMail.from_soledad(None, None, self._create_bdoc(raw="100% happy with percentage symbol"), parts=parts, soledad_querier=None)

        self.assertRegexpMatches(mail.text_plain_body, '([\s\S]*100%)')
        self.assertRegexpMatches(mail.html_body, '([\s\S]*100%)')

    def test_content_type_header_of_mail_part_is_used(self):
        plain_headers = {'Content-Type': 'text/plain; charset=utf-8', 'Content-Transfer-Encoding': 'quoted-printable'}
        html_headers = {'Content-Type': 'text/html; charset=utf-8', 'Content-Transfer-Encoding': 'quoted-printable'}
        parts = {'alternatives': [{'content': 'H=C3=A4llo', 'headers': plain_headers}, {'content': '<p>H=C3=A4llo</p>', 'headers': html_headers}]}

        mail = PixelatedMail.from_soledad(None, None, self._create_bdoc(raw='some raw body'), parts=parts, soledad_querier=None)

        self.assertEqual(2, len(mail.alternatives))
        self.assertEquals(u'H\xe4llo', mail.text_plain_body)
        self.assertEquals(u'<p>H\xe4llo</p>', mail.html_body)

    def test_clean_line_breaks_on_address_headers(self):
        many_recipients = 'One <one@mail.com>,\nTwo <two@mail.com>, Normal <normal@mail.com>,\nalone@mail.com'
        headers = {'Cc': many_recipients,
                   'Bcc': many_recipients,
                   'To': many_recipients}
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'],
                                                 extra_headers=headers)

        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)

        for header_label in ['To', 'Cc', 'Bcc']:
            for address in mail.headers[header_label]:
                self.assertNotIn('\n', address)
                self.assertNotIn(',', address)
            self.assertEquals(4, len(mail.headers[header_label]))

    def test_that_body_understands_base64(self):
        body = u'bl\xe1'
        encoded_body = unicode(body.encode('utf-8').encode('base64'))

        fdoc, hdoc, bdoc = test_helper.leap_mail()
        parts = {'alternatives': []}
        parts['alternatives'].append({'content': encoded_body, 'headers': {'Content-Transfer-Encoding': 'base64'}})
        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier, parts=parts)

        self.assertEquals(body, mail.text_plain_body)

    def _create_bdoc(self, raw):
        class FakeBDoc:
            def __init__(self, raw):
                self.content = {'raw': raw}
        return FakeBDoc(raw)


class InputMailTest(unittest.TestCase):
    mail_dict = lambda x: {
        'body': 'Este \xe9 o corpo',
        'header': {
            'cc': ['cc@pixelated.org', 'anothercc@pixelated.org'],
            'to': ['to@pixelated.org', 'anotherto@pixelated.org'],
            'bcc': ['bcc@pixelated.org', 'anotherbcc@pixelated.org'],
            'subject': 'Oi'
        },
        'ident': '',
        'tags': ['sent']
    }

    multipart_mail_dict = lambda x: {
        'body': [{'content-type': 'plain', 'raw': 'Hello world!'},
                 {'content-type': 'html', 'raw': '<p>Hello html world!</p>'}],
        'header': {
            'cc': ['cc@pixelated.org', 'anothercc@pixelated.org'],
            'to': ['to@pixelated.org', 'anotherto@pixelated.org'],
            'bcc': ['bcc@pixelated.org', 'anotherbcc@pixelated.org'],
            'subject': 'Oi',
        },
        'ident': '',
        'tags': ['sent']
    }

    def test_to_mime_multipart_should_add_blank_fields(self):
        pixelated.support.date.iso_now = lambda: 'date now'

        mail_dict = self.mail_dict()
        mail_dict['header']['to'] = ''
        mail_dict['header']['bcc'] = ''
        mail_dict['header']['cc'] = ''
        mail_dict['header']['subject'] = ''

        mime_multipart = InputMail.from_dict(mail_dict).to_mime_multipart()

        self.assertNotRegexpMatches(mime_multipart.as_string(), "\nTo: \n")
        self.assertNotRegexpMatches(mime_multipart.as_string(), "\nBcc: \n")
        self.assertNotRegexpMatches(mime_multipart.as_string(), "\nCc: \n")
        self.assertNotRegexpMatches(mime_multipart.as_string(), "\nSubject: \n")

    def test_to_mime_multipart(self):
        pixelated.support.date.iso_now = lambda: 'date now'

        mime_multipart = InputMail.from_dict(self.mail_dict()).to_mime_multipart()

        self.assertRegexpMatches(mime_multipart.as_string(), "\nTo: to@pixelated.org, anotherto@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nCc: cc@pixelated.org, anothercc@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nBcc: bcc@pixelated.org, anotherbcc@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nDate: date now\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nSubject: Oi\n")
        self.assertRegexpMatches(mime_multipart.as_string(), base64.b64encode(self.mail_dict()['body']))

    def test_smtp_format(self):
        InputMail.FROM_EMAIL_ADDRESS = 'pixelated@org'

        smtp_format = InputMail.from_dict(self.mail_dict()).to_smtp_format()

        self.assertRegexpMatches(smtp_format, "\nFrom: pixelated@org")

    def test_to_mime_multipart_handles_alternative_bodies(self):
        mime_multipart = InputMail.from_dict(self.multipart_mail_dict()).to_mime_multipart()

        part_one = 'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\nHello world!'
        part_two = 'Content-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n<p>Hello html world!</p>'

        self.assertRegexpMatches(mime_multipart.as_string(), part_one)
        self.assertRegexpMatches(mime_multipart.as_string(), part_two)
