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
        flags = self.leap_mail.getFlags()
        tags = set(Tag.from_flag(flag) for flag in flags)
        return tags

    def update_tags(self, tags):
        self.tags = [Tag(tag) for tag in tags]
        return self.tags

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

    @staticmethod
    def from_dict(mail_dict):
        return PixelatedMail()
