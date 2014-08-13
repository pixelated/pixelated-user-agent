import dateutil.parser as dateparser


class MailConverter:
    LEAP_FLAGS = ['\\Seen',
                  '\\Answered',
                  '\\Flagged',
                  '\\Deleted',
                  '\\Draft',
                  '\\Recent',
                  'List']

    def __init__(self, mail_service):
        pass

    def date_to_iso(self, date):
        return dateparser.parse(date).isoformat()

    def from_mail(self, imap_mail):

        headers = imap_mail.hdoc.content['headers']
        body = imap_mail.bdoc.content

        return {
            'header': {
                'from': [headers['From']],
                'to': [headers['To']],
                'cc': headers.get('CC', []),
                'bcc': headers.get('BCC', []),
                'date': self.date_to_iso(headers['Date']),
                'subject': headers['Subject']
            },
            'ident': imap_mail.getUID(),
            'tags': imap_mail.getFlags(),
            'status': [],
            'security_casing': {},
            'body': body['raw']
        }

    def to_mail(self, pixelated_mail, account):
        raise NotImplementedError()


    def from_tag(self, imap_tag):
        raise NotImplementedError()


    def from_contact(self, imap_contact):
        raise NotImplementedError()
