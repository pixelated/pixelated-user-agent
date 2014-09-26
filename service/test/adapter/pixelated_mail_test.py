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
import os

import pixelated.support.date
import test_helper
from pixelated.adapter.pixelated_mail import PixelatedMail, InputMail
from pixelated.adapter.tag_service import TagService
from pixelated.adapter.tag_index import TagIndex
from pixelated.adapter.tag import Tag
from mockito import *

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

    def test_update_tags_notifies_tag_service(self):
        db_path = '/tmp/test_update_tags_notifies_tag_service'
        tag_service = TagService(TagIndex(db_path))

        mail = PixelatedMail.from_soledad(*test_helper.leap_mail(), soledad_querier=self.querier)

        mail.update_tags({'new_tag'})
        self.assertIn(Tag('new_tag'), tag_service.all_tags())

        os.remove(db_path + '.db')

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
        PixelatedMail.from_email_address = 'pixelated@org'

        smtp_format = InputMail.from_dict(self.mail_dict()).to_smtp_format()

        self.assertRegexpMatches(smtp_format, "\nFrom: pixelated@org")