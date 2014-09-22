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
from pixelated.adapter.status import Status
from pixelated.support.id_gen import gen_pixelated_uid
from pixelated.adapter.tag_service import TagService
import json
import pixelated.support.date
import dateutil.parser as dateparser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class PixelatedMail:

    def __init__(self, fdoc, hdoc, bdoc):
        self.fdoc = fdoc
        self.hdoc = hdoc
        self.bdoc = bdoc

    @property
    def body(self):
        return self.bdoc.content['raw']

    @property
    def headers(self):
        _headers = {}
        for header in ['From', 'Date', 'Subject', 'Cc', 'Bcc']:
            _headers[header.lower()] = self.hdoc.content['headers'].get(header)
        return _headers

    @property
    def status(self):
        return Status.from_flags(self.fdoc.content.get('flags'))

    @property
    def security_casing(self):
        return {}

    @property
    def tags(self):
        mailbox_tag = self.hdoc.content.get('mbox', '').lower()
        tags = self.hdoc.content['headers'].get('x-tags', '[]')
        _tags = tags if type(tags) is list else json.loads(tags)  # this should go away since they should always be json'ed
        _tags.append(mailbox_tag)
        return set(_tags)

    @property
    def ident(self):
        return self.fdoc.content.get('chash')

    def as_dict(self):
        return {
            'header': self.headers,
            'ident': self.ident,
            'tags': list(self.tags),
            'status': [str(stat) for stat in self.status],
            'security_casing': self.security_casing,
            'body': self.body
        }