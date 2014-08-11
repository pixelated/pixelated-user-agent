from mail import Mail


class MailSet:

    def __init__(self):
        self.ident = 0
        self.mails = {}

    def add(self, mbox_mail):
        self.mails[self.ident] = Mail(mbox_mail)
        self.ident += 1


