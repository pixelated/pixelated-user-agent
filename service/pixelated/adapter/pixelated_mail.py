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
from pixelated.adapter.tag import Tag
from pixelated.adapter.status import Status
import dateutil.parser as dateparser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class PixelatedMail:

    def __init__(self):
        pass

    @staticmethod
    def from_leap_mail(leap_mail):
        mail = PixelatedMail()
        mail.leap_mail = leap_mail
        mail.body = leap_mail.bdoc.content['raw']
        mail.headers = mail._extract_headers()
        mail.date = dateparser.parse(mail.headers['date'])
        mail.ident = leap_mail.getUID()
        mail.status = mail._extract_status()
        mail.security_casing = {}
        mail.tags = mail._extract_tags()
        return mail

    def set_from(self, _from):
        self.headers['from'] = [_from]

    def get_to(self):
        return self.headers['to'][0]

    def _extract_status(self):
        return Status.from_flags(self.leap_mail.getFlags())

    def _extract_headers(self):
        temporary_headers = {}
        for header, value in self.leap_mail.hdoc.content['headers'].items():
            temporary_headers[header.lower()] = value
        if(temporary_headers.get('to') is not None):
            temporary_headers['to'] = [temporary_headers['to']]
        return temporary_headers

    def _extract_tags(self):
        return Tag.from_flags(self.leap_mail.getFlags())

    def update_tags(self, tags):
        old_tags = self.tags
        self.tags = tags
        removed_tags = old_tags.difference(self.tags)
        return self.tags, removed_tags

    def has_tag(self, tag):
        return Tag(tag) in self.tags

    def as_dict(self):
        tags = [tag.name for tag in self.tags]
        statuses = [status.name for status in self.status]
        return {
            'header': self.headers,
            'ident': self.ident,
            'tags': tags,
            'status': statuses,
            'security_casing': self.security_casing,
            'body': self.body
        }

    def to_mime_multipart(self):
        mime_multipart = MIMEMultipart()
        mime_multipart['To'] = self.headers['to'][0]
        mime_multipart['Subject'] = self.headers['subject']
        mime_multipart.attach(MIMEText(self.body, 'plain'))
        return mime_multipart

    def to_smtp_format(self, _from=None):
        mime_multipart = self.to_mime_multipart()
        mime_multipart['From'] = _from
        return mime_multipart.as_string()

    @staticmethod
    def from_dict(mail_dict):
        return from_dict(mail_dict)


def from_dict(mail_dict):
    mail = PixelatedMail()
    mail.headers = mail_dict['header']
    mail.body = mail_dict['body']
    mail.ident = mail_dict['ident']
    mail.tags = mail_dict['tags']
    return mail
