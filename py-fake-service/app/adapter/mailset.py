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
        return self.mails.get(mail_id)

    def mark_as_read(self, mail_id):
        mail = self.get(mail_id)
        mail.status.append('read')

    def delete(self, mail_id):
        """ Returns True if the email got purged, else returns False meaning the email got moved to trash """

        mail = self.get(mail_id)
        if 'trash' in mail.tags:
            del self.mails[mail_id]
            return True
        mail.tags.append('trash') 
        return False


