import unittest

from flask import json
from mockito import mock
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.pixelated_mailboxes import PixelatedMailBoxes
from pixelated.adapter.soledad_querier import SoledadQuerier
import pixelated.user_agent
from integration import JSONMailBuilder, initialize_soledad


class FakeAccount(object):
    def __init__(self):
        self.mailboxes = ['INBOX', 'DRAFTS', 'SENT', 'TRASH']


class MailFetchTest(unittest.TestCase):

    def setUp(self):
        self.soledad_test_folder = "soledad-test"
        self.app = pixelated.user_agent.app.test_client()
        self.account = FakeAccount()
        self.mail_sender = mock()
        self.mail_address = "test@pixelated.org"
        self.soledad = initialize_soledad(tempdir=self.soledad_test_folder)

        SoledadQuerier.get_instance(soledad=self.soledad)
        PixelatedMail.from_email_address = self.mail_address
        pixelated_mailboxes = PixelatedMailBoxes(self.account)
        pixelated.user_agent.mail_service = MailService(pixelated_mailboxes, self.mail_sender)
        pixelated.user_agent.DISABLED_FEATURES = []

    def tearDown(self):
        self.soledad.close()
        import shutil
        shutil.rmtree(self.soledad_test_folder)

    def get(self, url):
        return json.loads(self.app.get(url).data)

    def post_mail(self, data):
        self.app.post('/mails', data=data, content_type="application/json")

    def test_get_mails(self):
        mail_one = JSONMailBuilder().with_subject("Mail One").build()
        mail_two = JSONMailBuilder().with_subject("Mail Two").build()

        self.post_mail(mail_one)
        self.post_mail(mail_two)

        response = self.get('/mails?q=tag:drafts')

        # ordered by creation date
        self.assertEquals(u'Mail Two', response['mails'][0]['header']['subject'])
        self.assertEquals(u'Mail One', response['mails'][1]['header']['subject'])
