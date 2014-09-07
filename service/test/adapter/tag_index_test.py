
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

from pixelated.adapter.tag_index import TagIndex
from pixelated.adapter.tag import Tag


class TestTagIndex(unittest.TestCase):

    def setUp(self):
        self.db_path = '/tmp/database_test_tag_index'
        self.tag_index = TagIndex(self.db_path)

    def tearDown(self):
        self.tag_index.close_db()
        os.remove(self.db_path + '.db')

    def test_get_and_set_works(self):
        tag = Tag('a_tag')
        self.tag_index.set(tag)
        self.assertEquals(tag, self.tag_index.get('a_tag'))

    def test_values_returns_all_values_in_the_index(self):
        tag_a = Tag('tag_a')
        self.tag_index.set(tag_a)
        tag_b = Tag('tag_b')
        self.tag_index.set(tag_b)
        tag_c = Tag('tag_c')
        self.tag_index.set(tag_c)

        self.assertEquals(set([tag_a, tag_b, tag_c]), self.tag_index.values())

    def test_changes_are_visible_between_instances_using_same_file(self):
        tag = Tag('some_tag')
        self.tag_index.set(tag)

        other_tag_index = TagIndex(self.db_path)
        self.assertIn(tag, other_tag_index.values())

    def test_add_does_not_replace_existent_tag_with_same_name(self):
        tag = Tag('tag', True)
        self.tag_index.set(tag)

        same_name_tag = Tag('tag', False)
        self.tag_index.add(same_name_tag)

        self.assertEquals(True, self.tag_index.get('tag').default)

    def test_empty_returns_true_if_there_are_no_values(self):
        self.assertTrue(self.tag_index.empty())

    def test_empty_returns_false_if_there_are_values(self):
        self.tag_index.set(Tag('tag'))
        self.assertFalse(self.tag_index.empty())
