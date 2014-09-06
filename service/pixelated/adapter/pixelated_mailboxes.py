from pixelated.adapter.pixelated_mailbox import PixelatedMailbox


class PixelatedMailBoxes():
    def __init__(self, account):
        self.account = account
        self.mailbox_name = 'INBOX'

    def inbox(self):
        return PixelatedMailbox.create(self.account)

    @property
    def mailboxes(self):
        return [PixelatedMailbox.create(self.account, leap_mailbox_name) for leap_mailbox_name in
                self.account.mailboxes]

    def mails_by_tag(self, query_tags):
        mails = []
        for mailbox in self.mailboxes:
            mails.extend(mailbox.mails_by_tags(query_tags))

        return mails

    def leap_inbox_mailbox(self):
        return self.account.getMailbox(self.mailbox_name)
