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
            'cc': ['cc@pixelated.org'],
            'to': ['to@pixelated.org'],
            'subject': 'Oi',
            'bcc': ['bcc@pixelated.org']
        },
        'ident': '',
        'tags': ['sent']
    }

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

    def test_non_tags_flags_are_ignored(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(leap_flags=['\\Recent'],
                                                      extra_flags=['this_is_not_a_tag', 'tag_custom_tag']))
        self.assertEquals(set([Tag('custom_tag'), Tag('inbox')]), pixelated_mail.tags)

    def test_from_dict(self):

        mail = PixelatedMail.from_dict(self.mail_dict)

        self.assertEqual(mail.headers['cc'], ['cc@pixelated.org'])
        self.assertEqual(mail.headers['to'], ['to@pixelated.org'])
        self.assertEqual(mail.headers['bcc'], ['bcc@pixelated.org'])
        self.assertEqual(mail.headers['subject'], 'Oi')
        self.assertEqual(mail.ident, '')
        self.assertEqual(mail.tags, ['sent'])
        self.assertEqual(mail.body, 'Este \xe9 o corpo')

    def test_update_tags_return_a_set_for_current_tags_and_a_set_for_removed(self):
        pixelated_mail = PixelatedMail.from_leap_mail(test_helper.leap_mail(leap_flags=[], extra_flags=['tag_custom_1', 'tag_custom_2']))
        current_tags, removed_tags = pixelated_mail.update_tags(set([Tag('custom_1'), Tag('custom_3')]))
        self.assertEquals(set([Tag('custom_3'), Tag('custom_1')]), current_tags)
        self.assertEquals(set([Tag('custom_2')]), removed_tags)

    def test_to_mime_multipart(self):
        mail = PixelatedMail.from_dict(self.mail_dict)

        mime_multipart = mail.to_mime_multipart()

        self.assertRegexpMatches(mime_multipart.as_string(), "\nTo: to@pixelated.org\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nSubject: Oi\n")
        self.assertRegexpMatches(mime_multipart.as_string(), "\nEste \xe9 o corpo")

