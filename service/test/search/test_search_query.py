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
import sys
import os
import unittest
import pixelated.search_query as search_query


class SearchTestCase(unittest.TestCase):

    def test_one_tag(self):
        self.assertEquals(search_query.compile(u"in:inbox")["tags"], ["inbox"])
        self.assertEquals(search_query.compile(u"in:trash")["tags"], ["trash"])

    def test_two_tags_or(self):
        self.assertEquals(search_query.compile(u"in:inbox or in:trash")["tags"], ["inbox", "trash"])

    def test_tag_negate(self):
        self.assertEquals(search_query.compile(u"-in:trash")["not_tags"], ["trash"])

    def test_general_search(self):
        self.assertEquals(search_query.compile(u"searching")["general"], "searching")

    def test_tags_with_quotes(self):
        self.assertEquals(search_query.compile(u"in:\"inbox\"")["tags"], ["inbox"])
        self.assertEquals(search_query.compile(u"in:'inbox'")["tags"], ["inbox"])
