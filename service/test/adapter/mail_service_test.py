import sys
import os
import unittest
from mock import patch
from mock import Mock

from app.adapter.mail_service import MailService


class MailboxCollision(Exception):
    pass


class MailboxException(Exception):
    pass


class TestMailService(unittest.TestCase):

    def setUp(self):
        self.mail_service = MailService()

    def test_request_mail_has_mailbox(self):
        with patch.object(self.mail_service, '_switch_mailbox', return_value=Mock()):
            mails = self.mail_service.mails({'tags': ['inbox']})
            self.assertIsNotNone(mails)

    def test_request_mail_has_mailbox(self):
        with patch.object(self.mail_service, '_switch_mailbox', return_value=None):
            mails = self.mail_service.mails({'tags': ['inbox']})
            self.assertEqual(mails, [])

    def test_switch_mailbox_special_tag(self):
        mailbox = Mock()
        with patch.object(self.mail_service.account, 'getMailbox', return_value=mailbox):
            new_mailbox = self.mail_service._switch_mailbox('sent')
            self.assertEqual(new_mailbox, mailbox)

    def test_switch_mailbox_custom_tag_exists(self):
        mailbox = Mock()
        with patch.object(self.mail_service.account, 'getMailbox', return_value=mailbox):
            returned_mailbox = self.mail_service._switch_mailbox('custom')
            self.assertEqual(mailbox, returned_mailbox)

    def test_switch_mailbox_custom_tag_not_exists(self):
        mailbox = Mock()
        with patch.object(self.mail_service.account, 'getMailbox', side_effect=MailboxException()):
            mailbox = self.mail_service._switch_mailbox('custom')
            self.assertIsNone(mailbox)

    def test_create_new_mailbox(self):
        with patch.object(self.mail_service.account, 'addMailbox', return_value=True) as addMailbox:
            self.assertTrue(self.mail_service._create_mailbox('teste'))

    def test_create_existing_mailbox(self):
        with patch.object(self.mail_service.account, 'addMailbox', side_effect=MailboxCollision()) as addMailbox:
            self.assertFalse(self.mail_service._create_mailbox('teste'))
