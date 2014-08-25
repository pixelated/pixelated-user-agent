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
from pixelated.tags import Tags, Tag


class TagTestCase(unittest.TestCase):

    def test_create_tag(self):
        tag = Tag('test', True)
        self.assertEqual(tag.name, 'test')


class TagsTestCase(unittest.TestCase):

    def test_add_tag_to_collection(self):
        tag_collection = Tags()
        tag_collection.add('test')
        self.assertEqual(len(tag_collection), len(Tags()) + 1)
        tag_collection.add('test2')
        self.assertEqual(len(tag_collection), len(Tags()) + 2)

    def test_no_tag_duplication(self):
        tag_collection = Tags()
        tag_collection.add('test')
        self.assertEqual(len(tag_collection), len(Tags()) + 1)
        tag_collection.add('test')
        self.assertEqual(len(tag_collection), len(Tags()) + 1)

    def test_find_tag_on_collection(self):
        tag_collection = Tags()
        tag_collection.add('test')
        tag_collection.add('test2')
        self.assertEqual(tag_collection.find('test'), Tag('test', True))

    def test_special_tags_always_exist(self):
        special_tags = ['inbox', 'sent', 'drafts', 'trash']
        tag_collection = Tags()
        for tag in special_tags:
            self.assertIn(Tag(tag, True), tag_collection)

    def test_special_tags_are_default(self):
        tags = Tags()
        self.assertTrue(tags.find('inbox').default)
