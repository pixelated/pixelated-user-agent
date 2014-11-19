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
from pixelated.adapter.mail import PixelatedMail, InputMail
from mockito import *
from test.support import test_helper
import dateutil.parser as dateparser


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

    def test_as_dict(self):
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'])
        hdoc.content['headers']['Subject'] = 'The subject'
        hdoc.content['headers']['From'] = 'me@pixelated.org'

        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)

        _dict = mail.as_dict()

        self.assertEquals(_dict, {'body': 'body',
                                  'header': {
                                      'date': dateparser.parse(hdoc.content['date']).isoformat(),
                                      'from': 'me@pixelated.org',
                                      'subject': 'The subject'
                                  },
                                  'ident': 'chash',
                                  'mailbox': 'inbox',
                                  'security_casing': {'imprints': [], 'locks': []},
                                  'status': ['recent'],
                                  'tags': [],
                                  'attachments': []
                                  })

    def test_alternatives_body(self):
        parts = {'alternatives': [], 'attachments': []}
        parts['alternatives'].append({'content': 'blablabla', 'headers': {'Content-Type': 'text/plain'}})
        parts['alternatives'].append({'content': '<p>blablabla</p>', 'headers': {'Content-Type': 'text/html'}})

        mail = PixelatedMail.from_soledad(None, None, None, parts=parts, soledad_querier=None)

        self.assertRegexpMatches(mail.body, '^--' + mail.boundary + '\n.*')
        self.assertRegexpMatches(mail.body, '\nContent-Type: text/html\n\n<p>blablabla</p>\n')
        self.assertRegexpMatches(mail.body, '\nContent-Type: text/plain\n\nblablabla\n')
        self.assertRegexpMatches(mail.body, '.*--' + mail.boundary + '--$')

    def test_percent_character_is_allowed_on_body(self):
        parts = {'alternatives': [], 'attachments': []}
        parts['alternatives'].append({'content': '100% happy with percentage symbol', 'headers': {'Content-Type': 'text/plain'}})
        parts['alternatives'].append({'content': '<p>100% happy with percentage symbol</p>', 'headers': {'Content-Type': 'text/html'}})

        mail = PixelatedMail.from_soledad(None, None, None, parts=parts, soledad_querier=None)

        self.assertRegexpMatches(mail.body, '([\s\S]*100%){2}')

    def test_clean_line_breaks_on_address_headers(self):
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'])
        hdoc.content['headers']['To'] = 'One <one@mail.com>,\nTwo <two@mail.com>, Normal <normal@mail.com>,\nalone@mail.com'
        hdoc.content['headers']['Bcc'] = hdoc.content['headers']['To']
        hdoc.content['headers']['Cc'] = hdoc.content['headers']['To']

        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)

        for header_label in ['To', 'Cc', 'Bcc']:
            for address in mail.headers[header_label]:
                self.assertNotIn('\n', address)
                self.assertNotIn(',', address)
            self.assertEquals(4, len(mail.headers[header_label]))
    def test_to_reply_template_removes_user_from_to(self):
        InputMail.FROM_EMAIL_ADDRESS = 'user@pixelated.org'
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'])
        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)
        hdoc.content['headers']['To'] = ['me@pixelated.org', 'user@pixelated.org']

        template = mail.to_reply_template()

        self.assertFalse('user@pixelated.org' in template['header']['to'][0])

    def test_content_type_is_read_from_headers_for_plain_mail_when_converted_to_raw(self):
        fdoc, hdoc, bdoc = test_helper.leap_mail(flags=['\\Recent'], body=u'some umlaut \xc3', extra_headers={'Content-Type': 'text/plain; charset=ISO-8859-1'})
        hdoc.content['headers']['Subject'] = 'The subject'
        hdoc.content['headers']['From'] = 'me@pixelated.org'
        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self.querier)

        mail.raw


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
        self.assertRegexpMatches(mime_multipart.as_string(), "\nEste \xe9 o corpo")

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
