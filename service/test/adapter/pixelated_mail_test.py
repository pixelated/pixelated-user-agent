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

from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.tag import Tag
import test_helper


class TestPixelatedMail(unittest.TestCase):
    mail_dict = {
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

    def test_parse_date_from_leap_mail_uses_date_header_if_available(self):
        leap_mail_date = 'Wed, 3 Sep 2014 12:36:17 -0300'
        leap_mail_date_in_iso_format = "2014-09-03T12:36:17-03:00"

        leap_mail = test_helper.leap_mail(headers={'date': leap_mail_date})

        mail = PixelatedMail.from_leap_mail(leap_mail)

        self.assertEqual(str(mail.date), leap_mail_date_in_iso_format)

    def test_parse_date_from_leap_mail_fallback_to_received_header_if_date_header_isnt_available(self):
        leap_mail_date = "Wed, 03 Sep 2014 13:11:15 -0300"
        leap_mail_date_in_iso_format = "2014-09-03T13:11:15-03:00"
        leap_mail_received_header = "by bitmask.local from 127.0.0.1 with ESMTP ;\n " + leap_mail_date

        leap_mail = test_helper.leap_mail(headers={'received': leap_mail_received_header})

        mail = PixelatedMail.from_leap_mail(leap_mail)

        self.assertEqual(str(mail.date), leap_mail_date_in_iso_format)

    def test_from_dict(self):
        mail = PixelatedMail.from_dict(self.mail_dict)

        self.assertEqual(mail.headers['cc'], ['cc@pixelated.org', 'anothercc@pixelated.org'])
        self.assertEqual(mail.headers['to'], ['to@pixelated.org', 'anotherto@pixelated.org'])
        self.assertEqual(mail.headers['bcc'], ['bcc@pixelated.org', 'anotherbcc@pixelated.org'])
        self.assertEqual(mail.headers['subject'], 'Oi')
        self.assertEqual(mail.ident, '')
        self.assertEqual(mail.tags, ['sent'])
        self.assertEqual(mail.body, 'Este \xe9 o corpo')

    def test_update_tags_return_a_set_for_current_tags(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(extra_headers={'X-tags': ['custom_1', 'custom_2']}))
        current_tags = pixelated_mail.update_tags(set([Tag('custom_1'), Tag('custom_3')]))
        self.assertEquals(set([Tag('custom_3'), Tag('custom_1')]), current_tags)

    def test_to_mime_multipart(self):
        mail = PixelatedMail.from_dict(self.mail_dict)

        mime_multipart = mail.to_mime_multipart()

        self.assertRegexpMatches(mime_multipart.as_string(), "\nTo: to@pixelated.org, anotherto@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nCc: cc@pixelated.org, anothercc@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nBcc: bcc@pixelated.org, anotherbcc@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nSubject: Oi\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nEste \xe9 o corpo")

    def test_smtp_format(self):
        mail = PixelatedMail.from_dict(self.mail_dict)

        smtp_format = mail.to_smtp_format(_from='pixelated@org')

        self.assertRegexpMatches(smtp_format, "\nFrom: pixelated@org")
