import unittest

from integration import JSONMailBuilder, SoledadTestBase


class MailFetchTest(unittest.TestCase, SoledadTestBase):

    def setUp(self):
        self.setup_soledad()

    def tearDown(self):
        self.teardown_soledad()

    def test_get_mails(self):
        mail_one = JSONMailBuilder().with_subject("Mail One").build()
        mail_two = JSONMailBuilder().with_subject("Mail Two").build()

        self.post_mail(mail_one)
        self.post_mail(mail_two)

        response = self.get_mails_by_tag("drafts")

        # ordered by creation date
        self.assertEquals(u'Mail Two', response['mails'][0]['header']['subject'])
        self.assertEquals(u'Mail One', response['mails'][1]['header']['subject'])
