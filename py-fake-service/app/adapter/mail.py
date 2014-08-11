from datetime import datetime

class Mail:

    def __init__(self, mbox_mail, ident):
        self.header = self._get_headers(mbox_mail)
        self.ident = ident
        self.body = mbox_mail.get_payload()
        self.tags = self._get_tags(mbox_mail)
        self.security_casing = {}
        self.status = []

    def _get_headers(self, mbox_mail):
        headers = {}
        headers['from'] = mbox_mail.get_from()
        headers['to'] = [mbox_mail.items()['To']]
        headers['subject'] = mbox_mail.items()['Subject']
        headers['date'] = datetime.fromtimestamp(random.randrange(1222222222, 1444444444)).isoformat()
        return headers

    def _get_tags(self, mbox_mail):
        return mbox_mail.items()['X-TW-Pixelated-Tags'].split(', ')

    

        
