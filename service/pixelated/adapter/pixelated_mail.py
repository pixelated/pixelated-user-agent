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
# MERCHANTABILITY or FITNESS FOR A PCULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from pixelated.adapter.status import Status
from pixelated.support.id_gen import gen_pixelated_uid
from pixelated.adapter.tag_service import TagService
import json
import pixelated.support.date
import dateutil.parser as dateparser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class PixelatedMail:

    def __init__(self, tag_service=TagService.get_instance()):
        self.tag_service = tag_service
        self.mailbox_name = None
        self.querier = SoledadQuerier.get_instance()

    @staticmethod
    def from_soledad(fdoc, hdoc, bdoc):
        mail = PixelatedMail()
        mail.bdoc = bdoc
        mail.fdoc = fdoc
        mail.hdoc = hdoc
        return mail

    @property
    def body(self):
        return self.bdoc.content['raw']

    @property
    def headers(self):
        _headers = ['From', 'Date', 'Subject', 'Cc', 'Bcc']
        _headers = {header.lower(): self.hdoc.content['headers'].get(header) for header in _headers}
        map(lambda header: self._split_recipients(header, _headers), ['to', 'bcc', 'cc'])
        return _headers

    @property
    def status(self):
        return Status.from_flags(self.fdoc.content.get('flags'))

    @property
    def security_casing(self):
        return {}

    @property
    def tags(self):
        _tags = self.headers.get('x-tags', '[]')
        return set(_tags) if type(_tags) is list else set(json.loads(_tags))

    @property
    def ident(self):
        return self.fdoc.content.get('chash')

    @property
    def mailbox_name(self):
        return self.fdoc.content.get('mbox')

    @property
    def is_recent(self):
        return Status('recent') in self.status

    def save(self):
        return self.querier.save_mail(self)

    def set_from(self, _from):
        self.headers['from'] = [_from]

    def get_to(self):
        return self.headers['to']

    def get_cc(self):
        return self.headers['cc']

    def get_bcc(self):
        return self.headers['bcc']

    def _split_recipients(self, header_type, temporary_headers):
        if(temporary_headers.get(header_type) is not None):
            recipients = temporary_headers[header_type].split(',')
            temporary_headers[header_type] = map(lambda x: x.lstrip(), recipients)

    def mark_as_deleted(self):
        # self.remove_all_tags()
        # self.leap_mail.setFlags((Status.PixelatedStatus.DELETED,), 1)
        pass

    def remove_all_tags(self):
        self.update_tags(set([]))

    def update_tags(self, tags):
        old_tags = self.tags
        self.tags = tags
        removed = old_tags.difference(tags)
        added = tags.difference(old_tags)
        self._persist_mail_tags(tags)
        self.tag_service.notify_tags_updated(added, removed, self.ident)
        return self.tags

    def mark_as_read(self):
        # self.leap_mail.setFlags((Status.PixelatedStatus.SEEN,), 1)
        # self.status = self._extract_status()
        # return self
        pass

    def mark_as_not_recent(self):
        # self.leap_mail.setFlags((Status.PixelatedStatus.RECENT,), -1)
        # self.status = self._extract_status()
        # return self
        pass

    def _persist_mail_tags(self, current_tags):
        self.hdoc.content['headers']['X-Tags'] = json.dumps(list(current_tags))
        self.save()

    def has_tag(self, tag):
        return tag in self.tags

    def raw_message(self):
        mime = MIMEMultipart()
        for key, value in self.hdoc.content['headers'].items():
            mime[key] = value
        mime.attach(MIMEText(self.bdoc.content['raw'], 'plain'))
        return mime.as_string()

    def as_dict(self):
        statuses = [status.name for status in self.status]
        return {
            'header': self.headers,
            'ident': self.ident,
            'tags': list(self.tags),
            'status': statuses,
            'security_casing': self.security_casing,
            'body': self.body
        }

    def to_mime_multipart(self):
        mime_multipart = MIMEMultipart()

        for header in ['To', 'Cc', 'Bcc']:
            if self.headers[header.lower()]:
                mime_multipart[header] = ", ".join(self.headers[header.lower()])

        if self.headers['subject']:
            mime_multipart['Subject'] = self.headers['subject']

        mime_multipart['Date'] = self.headers['date']
        mime_multipart.attach(MIMEText(self.body, 'plain'))
        return mime_multipart

    def to_smtp_format(self):
        mime_multipart = self.to_mime_multipart()
        mime_multipart['From'] = PixelatedMail.from_email_address
        return mime_multipart.as_string()

    @staticmethod
    def from_dict(mail_dict):
        return from_dict(mail_dict)

    @classmethod
    def _get_date(cls, headers):
        date = headers.get('date', None)
        if not date:
            date = headers['received'].split(";")[-1].strip()
        return dateparser.parse(date).isoformat()


def from_dict(mail_dict):
    mail = PixelatedMail()
    mail.headers = mail_dict.get('header', {})
    mail.headers['date'] = pixelated.support.date.iso_now()
    mail.body = mail_dict.get('body', '')
    mail._ident = mail_dict.get('ident', None)
    mail.tags = set(mail_dict.get('tags', []))
    mail.status = set(mail_dict.get('status', []))
    return mail


from pixelated.adapter.soledad_querier import SoledadQuerier
