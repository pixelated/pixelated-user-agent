

class DraftService(object):
    __slots__ = '_mailboxes'

    def __init__(self, mailboxes):
        self._mailboxes = mailboxes

    def create_draft(self, input_mail):
        self._drafts().add(input_mail)
        return input_mail

    def update_draft(self, ident, input_mail):
        new_mail = self.create_draft(input_mail)
        self._drafts().remove(ident)
        return new_mail

    def _drafts(self):
        return self._mailboxes.drafts()
