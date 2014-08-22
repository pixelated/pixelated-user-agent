import unittest

from pixelated.adapter.mail_service import MailService
from mock import Mock, MagicMock, patch
import test_helper
from pixelated.tags import Tag


class TestMailService(unittest.TestCase):

    @patch.object(MailService, 'set_flags', return_value=None)
    def test_custom_tags_get_created_if_not_exists(self, mockSetFlags):
        MailService._open_leap_session = lambda self: None
        MailService.mailbox = Mock(messages=[test_helper.leap_mail(uid=6, leap_flags=['\\Recent'])])
        MailService.account = Mock(return_value=MagicMock())

        mailservice = MailService()

        new_tags = ['test', 'inbox']
        updated_tags = mailservice.update_tags(6, new_tags)

        self.assertEquals(set([Tag('test'), Tag('inbox')]), set(updated_tags))
        # make sure that special tags are skipped when setting leap flags (eg.: tag_inbox)
        mockSetFlags.assert_called_with(6, ['tag_test'])
