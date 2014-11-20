from nose.twistedtools import deferred
from test.support.integration import SoledadTestBase, MailBuilder


class SearchTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    @deferred(timeout=SoledadTestBase.DEFERRED_TIMEOUT)
    def test_that_tags_returns_all_tags(self):
        input_mail = MailBuilder().with_tags(['important']).build_input_mail()
        self.client.add_mail_to_inbox(input_mail)

        d = self.get_contacts(query='recipient')

        def _assert(contacts):
            self.assertTrue('recipient@to.com' in contacts)
            self.assertTrue('recipient@cc.com' in contacts)
            self.assertTrue('recipient@bcc.com' in contacts)
        d.addCallback(_assert)
        return d