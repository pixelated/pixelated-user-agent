from datetime import datetime
import random
import calendar

class Mail:

    NOW = calendar.timegm(datetime.strptime(datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f").timetuple())
    @staticmethod
    def from_json(mail_json):
        mail = Mail()
        mail.header = mail_json['header']
        mail.header['date'] = datetime.now().isoformat()
        mail.ident = mail_json.get('ident', 0)
        mail.body = mail_json['body']
        mail.tags = mail_json['tags']
        mail.security_casing = {}
        mail.status = []
        mail.draft_reply_for = mail_json.get('draft_reply_for', 0)
        return mail

            
    def __init__(self, mbox_mail=None, ident=None):
        if mbox_mail:
            self.header = self._get_headers(mbox_mail)
            self.ident = ident
            self.body = mbox_mail.get_payload()
            self.tags = self._get_tags(mbox_mail)
            self.security_casing = {}
            self.status = self._get_status()
            self.draft_reply_for = -1

    def _get_status(self):
        status = []
        if 'sent' in self.tags:
            status.append('read')

        return status

    def _get_headers(self, mbox_mail):
        headers = {}
        headers['from'] = mbox_mail.get_from()
        headers['to'] = [mbox_mail.get('To')]
        headers['subject'] = mbox_mail.get('Subject')
        headers['date'] = datetime.fromtimestamp(random.randrange(1222222222, self.NOW)).isoformat()
        return headers

    def _get_tags(self, mbox_mail):
        return mbox_mail.get('X-TW-Pixelated-Tags').split(', ')

        
    @property
    def subject(self):
        return self.header['subject']

    @property
    def date(self):
        return self.header['date']
