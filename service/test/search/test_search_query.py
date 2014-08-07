import sys
import os
import unittest
from app.search import SearchQuery


class SearchTestCase(unittest.TestCase):

    def test_one_tag(self):
        self.assertEquals(SearchQuery.compile(u"in:inbox")["tags"], ["inbox"])
        self.assertEquals(SearchQuery.compile(u"in:trash")["tags"], ["trash"])

    def test_two_tags_or(self):
        self.assertEquals(SearchQuery.compile(u"in:inbox or in:trash")["tags"], ["inbox", "trash"])

    def test_tag_negate(self):
        self.assertEquals(SearchQuery.compile(u"-in:trash")["not_tags"], ["trash"])

    def test_general_search(self):
        self.assertEquals(SearchQuery.compile(u"searching")["general"], "searching")

    def test_tags_with_quotes(self):
        self.assertEquals(SearchQuery.compile(u"in:\"inbox\"")["tags"], ["inbox"])
        self.assertEquals(SearchQuery.compile(u"in:'inbox'")["tags"], ["inbox"])
