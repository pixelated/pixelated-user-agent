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
