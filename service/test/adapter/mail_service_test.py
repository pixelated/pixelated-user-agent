import sys
import os
import unittest

from app.adapter.mail_service import MailService


class TestMailService(unittest.TestCase):

    def test_initialization(self):
        mail_service = MailService()

    def test_receive_mail(self):
        mail_service = MailService()
        mails = mail_service.mails("")
        self.assertIsNotNone(mails)
