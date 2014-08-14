import unittest

from app.adapter.mail_service import MailService
from mock import Mock, MagicMock, patch
import test_helper
from app.tags import Tag


class TestMailService(unittest.TestCase):

    def _raw_mail(self):
        return {
            "header":
                {
                    "to": ["p@k.s"],
                    "from": "a@y.t",
                    "subject": "Test",
                    "date": "2007-09-28T06:11:03-03:00"
                },
            "ident": 6,
            "tags": ["instagramer"],
            "status": [],
            "security_casing": {},
            "draft_reply_for": [],
            "body": "teste"
        }

    def test_custom_tags_get_created_if_not_exists(self):
        MailService._open_leap_session = lambda self: None
        MailService.mailbox = Mock(messages=[test_helper.leap_mail(uid=6)])
        MailService.account = Mock(return_value=MagicMock())

        mailservice = MailService()

        new_tags = ['test']
        mails = mailservice.update_tags(6, new_tags)

        for tag in mailservice.all_tags():
            print tag.name

        self.assertIn(Tag('test'), mailservice.all_tags())
