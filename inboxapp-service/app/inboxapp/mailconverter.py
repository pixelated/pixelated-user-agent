from inboxapp import Client
from datetime import datetime
import calendar


class MailConverter:

    def __init__(self, client):
        self.client = client

    def _from_epoch(self, epoch):
        return datetime.fromtimestamp(epoch).isoformat()

    def _to_epoch(self, iso8601):
        return calendar.timegm(
            datetime.strptime(iso8601, "%Y-%m-%dT%H:%M:%S.%f").timetuple()
        )

    def _to_contacts(self, pixelated_contacts):
        return [{"name": "", "email": x} for x in pixelated_contacts]

    def _from_contacts(self, inbox_contacts):
        return [contact['email'] for contact in inbox_contacts]

    def from_mail(self, inbox_mail):
        tags = sorted(self.client.tags_for_thread(inbox_mail['thread']))
        status = [] if "unread" in tags else ["read"]
        return {
            'header': {
                'from': inbox_mail['from'][0]['email'],
                'to': self._from_contacts(inbox_mail['to']),
                'cc': self._from_contacts(inbox_mail['cc']),
                'bcc': self._from_contacts(inbox_mail['bcc']),
                'date': self._from_epoch(inbox_mail['date']),
                'subject': inbox_mail['subject']
            },
            'ident': inbox_mail['id'],
            'tags': tags,
            'status': status,
            'security_casing': {},
            'body': inbox_mail['body'],
        }

    def to_mail(self, pixelated_mail, account):
        mail = {
            "to": self._to_contacts(pixelated_mail['header']['to']),
            "cc": self._to_contacts(pixelated_mail['header']['cc']),
            "bcc": self._to_contacts(pixelated_mail['header']['bcc']),
            "from": account,
            "body": pixelated_mail["body"],
            "subject": pixelated_mail["header"]["subject"],
            "date": self._to_epoch(datetime.now().isoformat()),
            "id": pixelated_mail["ident"],
            "object": "message",
        }
        if "draft_reply_for" in pixelated_mail:
            referred_mail = self.client.mail(pixelated_mail["draft_reply_for"])
            mail["reply_to_thread"] = referred_mail["thread"]
        return mail

    def from_tag(self, inbox_tag):
        default_tags = ["inbox", "sent", "trash", "drafts"]
        return {
            'name': inbox_tag['name'],
            'ident': inbox_tag['id'],
            'default': inbox_tag['name'] in default_tags,
            'counts': {
                'total': 0,
                'read': 0,
                'starred': 0,
                'reply': 0
            }
        }

    def from_contact(self, inbox_contact):
        return {
            'ident': inbox_contact['id'],
            'name': inbox_contact['name'],
            'addresses': [inbox_contact['email']],
            'mails_received': 0,
            'mails_sent': 0,
            'last_received': None,
            'last_sent': None
        }
