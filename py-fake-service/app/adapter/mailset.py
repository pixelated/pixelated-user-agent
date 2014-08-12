from mail import Mail


class MailSet:

    def __init__(self):
        self.ident = 0
        self.mails = {}

    def add(self, mbox_mail):
        self.mails[self.ident] = Mail(mbox_mail, self.ident)
        self.ident += 1

    def values(self):
        return self.mails.values()

    def get(self, mail_id):
        return self.mails.get(int(mail_id))

    def mark_as_read(self, mail_id):
        mail = self.mails.get(int(mail_id))
        mail.status.append('read')
