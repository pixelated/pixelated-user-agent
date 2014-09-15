from pixelated.adapter.pixelated_mailbox import PixelatedMailbox


class PixelatedMailBoxes():
    def __init__(self, account):
        self.account = account

    @property
    def mailboxes(self):
        return [PixelatedMailbox.create(self.account, leap_mailbox_name) for leap_mailbox_name in
                self.account.mailboxes]

    def mails_by_tag(self, query_tags):
        mails = []
        for mailbox in self.mailboxes:
            mails.extend(mailbox.mails_by_tags(query_tags))

        return mails

    def mail(self, mail_id):
        for mailbox in self.mailboxes:
            mail = mailbox.mail(mail_id)
            if mail:
                return mail

    def mailbox_exists(self, name):
        return name.upper() in map(lambda x: x.upper(), self.account.mailboxes)

    def trash(self):
        if not self.mailbox_exists('TRASH'):
            self.account.addMailbox('TRASH')
        return PixelatedMailbox.create(self.account, 'TRASH')
