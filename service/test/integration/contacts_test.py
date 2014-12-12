from nose.twistedtools import deferred
from test.support.integration import SoledadTestBase, MailBuilder


class ContactsTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    @deferred(timeout=SoledadTestBase.DEFERRED_TIMEOUT)
    def test_TO_CC_and_BCC_fields_are_being_searched(self):
        input_mail = MailBuilder().with_tags(['important']).build_input_mail()
        self.client.add_mail_to_inbox(input_mail)

        d = self.get_contacts(query='recipient')

        def _assert(contacts):
            self.assertTrue('recipient@to.com' in contacts)
            self.assertTrue('recipient@cc.com' in contacts)
            self.assertTrue('recipient@bcc.com' in contacts)
        d.addCallback(_assert)
        return d

    @deferred(timeout=SoledadTestBase.DEFERRED_TIMEOUT)
    def test_trash_and_drafts_mailboxes_are_being_ignored(self):
        self.client.add_multiple_to_mailbox(1, mailbox='INBOX', to='recipient@inbox.com')
        self.client.add_multiple_to_mailbox(1, mailbox='DRAFTS', to='recipient@drafts.com')
        self.client.add_multiple_to_mailbox(1, mailbox='SENT', to='recipient@sent.com')
        self.client.add_multiple_to_mailbox(1, mailbox='TRASH', to='recipient@trash.com')

        d = self.get_contacts(query='recipient')

        def _assert(contacts):
            self.assertTrue('recipient@inbox.com' in contacts)
            self.assertTrue('recipient@sent.com' in contacts)
            self.assertFalse('recipient@drafts.com' in contacts)
            self.assertFalse('recipient@trash.com' in contacts)
        d.addCallback(_assert)
        return d
