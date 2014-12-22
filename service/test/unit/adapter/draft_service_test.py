import unittest

from pixelated.adapter.model.mail import InputMail
from pixelated.adapter.services.draft_service import DraftService
import test.support.test_helper as test_helper
from mockito import *


class DraftServiceTest(unittest.TestCase):

    def setUp(self):
        self.mailboxes = mock()
        self.drafts_mailbox = mock()
        self.draft_service = DraftService(self.mailboxes)
        when(self.mailboxes).drafts().thenReturn(self.drafts_mailbox)

    def test_add_draft(self):
        mail = InputMail()
        self.draft_service.create_draft(mail)

        verify(self.drafts_mailbox).add(mail)

    def test_update_draft(self):
        mail = InputMail.from_dict(test_helper.mail_dict())
        when(self.drafts_mailbox).add(mail).thenReturn(mail)

        self.draft_service.update_draft(mail.ident, mail)

        inorder.verify(self.drafts_mailbox).add(mail)
        inorder.verify(self.drafts_mailbox).remove(mail.ident)
