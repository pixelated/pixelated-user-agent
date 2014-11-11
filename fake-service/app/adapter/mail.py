#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime
import random
import calendar
from dateutil import parser


class Mail:

    NOW = calendar.timegm(
        datetime.strptime(
            datetime.now().isoformat(),
            "%Y-%m-%dT%H:%M:%S.%f").timetuple())

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
        attachments = [{'headers': {'Content-Type': 'application/pdf',
                                    'Content-Transfer-Encoding': 'base64'},
                        'ident': 'BEBACAFE04090',
                        'name': 'mydoc.pdf'},
                       {'headers': {'Content-Type': 'application/pdf',
                                    'Content-Transfer-Encoding': 'base64'},
                        'ident': 'BEBACAFE04091',
                        'name': 'Party Pictures.jpg'}]
        if mbox_mail:
            self.header = self._get_headers(mbox_mail)
            self.ident = ident
            self.body = self._get_body(mbox_mail)
            self.tags = self._get_tags(mbox_mail)
            self.security_casing = {}
            self.status = self._get_status()
            self.draft_reply_for = -1
            self.attachments = attachments

    def _get_body(self, message):
        if message.is_multipart():
            boundary = '--{boundary}'.format(
                boundary=message.get_boundary().strip())
            body_parts = [x.as_string() for x in message.get_payload()]

            body = boundary + '\n'
            body += '{boundary}\n'.format(boundary=boundary).join(body_parts)
            body += '{boundary}--\n'.format(boundary=boundary)

            return body
        else:
            return message.get_payload()

    def _get_status(self):
        status = []
        if 'sent' in self.tags:
            status.append('read')

        return status

    def _get_headers(self, mbox_mail):
        headers = {}
        headers['from'] = mbox_mail.get('From') or mbox_mail.from_addr
        headers['to'] = [mbox_mail.get('To')]
        headers['subject'] = mbox_mail.get('Subject')
        headers['date'] = self._get_date(mbox_mail)
        headers['content_type'] = mbox_mail.get('Content-Type')

        return headers

    def _get_date(self, mbox_mail):
        random_date = datetime.fromtimestamp(random.randrange(1222222222, self.NOW)).isoformat()
        mbox_date = mbox_mail.get('Date')

        if not mbox_date:  # means we are still using the mailsets - important for functional tests
            return random_date
        return parser.parse(mbox_mail['Date']).isoformat()

    def _get_tags(self, mbox_mail):
        return filter(len, mbox_mail.get('X-TW-Pixelated-Tags').split(', '))

    @property
    def subject(self):
        return self.header['subject']

    @property
    def date(self):
        return self.header['date']
