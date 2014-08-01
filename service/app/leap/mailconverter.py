class MailConverter:

    def __init__(self, client):
        pass

    def from_mail(self, inbox_mail):
        raise NotImplementedError()


    def to_mail(self, pixelated_mail, account):
        raise NotImplementedError()


    def from_tag(self, inbox_tag):
        raise NotImplementedError()


    def from_contact(self, inbox_contact):
        raise NotImplementedError()


