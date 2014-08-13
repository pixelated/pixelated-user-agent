import unittest

from app.adapter.mail_service import MailService


class MailboxCollision(Exception):
    pass


class MailboxException(Exception):
    pass


class TestMailService(unittest.TestCase):

    def setUp(self):
        self.mail_service = MailService()
