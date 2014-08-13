import unittest

from app.adapter.pixelated_mail import PixelatedMail
from mock import Mock
from app.tags import Tag


class TestPixelatedMail(unittest.TestCase):

    LEAP_FLAGS = ['\\Seen',
                  '\\Answered',
                  '\\Flagged',
                  '\\Deleted',
                  '\\Draft',
                  '\\Recent',
                  'List']

    def setUp(self):
        self.leap_mail = Mock(getUID=Mock(return_value=0),
                              getFlags=Mock(return_value=self.LEAP_FLAGS),
                              bdoc=Mock(content={'raw': 'test'}),
                              hdoc=Mock(content={'headers': {}}))

    def test_leap_flags_that_are_tags_are_handled(self):
        pixelated_mail = PixelatedMail(self.leap_mail)
        self.assertIn(Tag('inbox'), pixelated_mail.tags)
        self.assertIn(Tag('trash'), pixelated_mail.tags)
        self.assertIn(Tag('drafts'), pixelated_mail.tags)

    def test_leap_flags_that_are_status_are_handled(self):
        pixelated_mail = PixelatedMail(self.leap_mail)
        self.assertIn('read', pixelated_mail.status)
        self.assertIn('replied', pixelated_mail.status)
