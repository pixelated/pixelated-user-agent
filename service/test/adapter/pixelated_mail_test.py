import unittest

from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.tags import Tag
from pixelated.tags import Tags
import test_helper


class TestPixelatedMail(unittest.TestCase):

    def test_leap_flags_that_are_tags_are_handled(self):
        pixelated_mail = PixelatedMail(test_helper.leap_mail())
        self.assertIn(Tag('inbox'), pixelated_mail.tags)
        self.assertIn(Tag('trash'), pixelated_mail.tags)
        self.assertIn(Tag('drafts'), pixelated_mail.tags)

    def test_leap_flags_that_are_status_are_handled(self):
        pixelated_mail = PixelatedMail(test_helper.leap_mail())
        self.assertIn('read', pixelated_mail.status)
        self.assertIn('replied', pixelated_mail.status)

    def test_leap_flags_that_are_custom_tags_are_handled(self):
        pixelated_mail = PixelatedMail(test_helper.leap_mail(extra_flags=['tag_work']))
        self.assertIn(Tag('work'), pixelated_mail.tags)

    def test_custom_tags_containing_our_prefix_are_handled(self):
        pixelated_mail = PixelatedMail(test_helper.leap_mail(extra_flags=['tag_tag_work_tag_']))
        self.assertIn(Tag('tag_work_tag_'), pixelated_mail.tags)
