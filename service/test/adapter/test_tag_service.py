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
import tempfile
import test_helper
from pixelated.adapter.tag import Tag
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.tag_index import TagIndex
from pixelated.adapter.tag_service import TagService


class TagServiceTest(unittest.TestCase):
    def setUp(self):
        self.index_file_handler, self.index_file_path = tempfile.mkstemp()
        self.tag_index = TagIndex(self.index_file_path)
        self.tag_service = TagService(tag_index=self.tag_index)

    def test_index_is_initialized_with_mail_tags_if_empty(self):
        mail_one = PixelatedMail.from_leap_mail(test_helper.leap_mail(uid=0, extra_headers={'X-Tags': ['tag_1']}))
        mail_two = PixelatedMail.from_leap_mail(test_helper.leap_mail(uid=1, extra_headers={'X-Tags': ['tag_2']}))
        mails = [mail_one, mail_two]

        self.tag_service.load_index(mails)

        self.assertEqual(self.tag_service.all_tags(), {Tag('sent'), Tag('inbox'), Tag('drafts'), Tag('trash'), Tag('tag_1'), Tag('tag_2')})

    def test_special_tags_always_exists(self):
        self.tag_service.load_index([])

        self.assertEqual(self.tag_service.all_tags(), {Tag('sent'), Tag('inbox'), Tag('drafts'), Tag('trash')})

    def test_notify_tags_updated_method_properly_changes_tags_state(self):
        mail_ident = 12
        tag = Tag('one_tag')
        tag.increment(mail_ident)
        self.tag_service.load_index([])
        self.tag_service.tag_index.set(tag)

        self.assertEquals(0, self.tag_service.tag_index.get('inbox').total)
        self.assertEquals(1, self.tag_service.tag_index.get('one_tag').total)

        self.tag_service.notify_tags_updated(set(['inbox']), set(['one_tag']), mail_ident)

        self.assertEquals(1, self.tag_service.tag_index.get('inbox').total)
        self.assertIsNone(self.tag_service.tag_index.get('one_tag'))
