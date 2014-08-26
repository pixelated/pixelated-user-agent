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
from pixelated.adapter.status import Status
import test_helper


class TestPixelatedMail(unittest.TestCase):

    def test_leap_recent_flag_is_translated_to_inbox_tag(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(leap_flags=['\\Recent']))
        self.assertIn(Tag('inbox'), pixelated_mail.tags)

    def test_leap_deleted_flag_is_translated_to_trash_tag(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(leap_flags=['\\Deleted']))
        self.assertIn(Tag('trash'), pixelated_mail.tags)

    def test_leap_draft_flag_is_translated_to_draft_tag(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(leap_flags=['\\Draft']))
        self.assertIn(Tag('drafts'), pixelated_mail.tags)

    def test_leap_flags_that_are_custom_tags_are_handled(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(extra_flags=['tag_work']))
        self.assertIn(Tag('work'), pixelated_mail.tags)

    def test_custom_tags_containing_our_prefix_are_handled(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(extra_flags=['tag_tag_work_tag_']))
        self.assertIn(Tag('tag_work_tag_'), pixelated_mail.tags)

    def from_dict(self):
        mail_dict = {
            'body': 'Este \xe9 o corpo',
            'header': {
                'cc': ['cc@pixelated.com'],
                'to': ['to@pixelated.com'],
                'subject': 'Oi',
                'bcc': ['bcc@pixelated.com']
            },
            'ident': '',
            'tags': ['sent']
        }

        mail = PixelatedMail.from_dict(mail_dict)

        self.assertEqual(mail.headers.cc, ['cc@pixelated.com'])
        self.assertEqual(mail.headers.to, ['to@pixelated.com'])
        self.assertEqual(mail.headers.bcc, ['bcc@pixelated.com'])
        self.assertEqual(mail.headers.subject, 'Oi')
        self.assertEqual(mail.ident, '')
        self.assertEqual(mail.tags, ['sent'])
        self.assertEqual(mail.body, 'Este \xe9 o corpo')
