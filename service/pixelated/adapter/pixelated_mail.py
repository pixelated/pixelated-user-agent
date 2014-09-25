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
import json

from leap.mail.imap.fields import fields
import leap.mail.walk as walk
import dateutil.parser as dateparser
from pixelated.adapter.status import Status
from pixelated.adapter.tag_service import TagService
import pixelated.support.date
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from pycryptopp.hash import sha256
from pixelated.support.functional import flatten


class InputMail:

    def __init__(self):
        self._raw_message = None
        self._fd = None
        self._hd = None
        self._bd = None
        self._mime = None

    def as_dict(self):
        statuses = [status.name for status in self.status]
        return {
            'header': self.headers,
            'ident': self.ident,
            'tags': list(self.tags),
            'status': statuses,
            'security_casing': {},
            'body': self.body
        }


    @staticmethod
    def from_dict(mail_dict):
        input_mail = InputMail()
        input_mail.headers = {key.capitalize(): value for key, value in mail_dict['header'].items()}
        input_mail.headers['Date'] = pixelated.support.date.iso_now()
        input_mail.body = mail_dict['body']
        input_mail.tags = set(mail_dict.get('tags', []))
        input_mail.status = set(mail_dict.get('status', []))
        return input_mail

    @property
    def _mime_multipart(self):
        if self._mime:
            return self._mime
        mime = MIMEMultipart()
        for key, value in self.headers.items():
            mime[str(key)] = str(value)
        mime.attach(MIMEText(self.body, 'plain'))
        self._mime = mime
        return mime

    @property
    def ident(self):
        return self._get_chash()

    def _raw(self):
        if self._raw_message:
            return self._raw_message
        self._raw_message = self._mime_multipart.as_string()
        return self._raw_message

    def _get_chash(self):
        return sha256.SHA256(self._raw()).hexdigest()

    def _get_for_save(self, next_uid):
        docs = [self._fdoc(next_uid), self._hdoc()]
        docs.extend([m for m in self._cdocs()])
        return docs

    def _fdoc(self, next_uid):
        if self._fd:
            return self._fd

        fd = {}
        fd[fields.MBOX_KEY] = 'DRAFTS'
        fd[fields.UID_KEY] = next_uid
        fd[fields.CONTENT_HASH_KEY] = self._get_chash()
        fd[fields.SIZE_KEY] = len(self._raw())
        fd[fields.MULTIPART_KEY] = True
        fd[fields.RECENT_KEY] = True
        fd[fields.TYPE_KEY] = fields.TYPE_FLAGS_VAL
        fd[fields.FLAGS_KEY] = []
        self._fd = fd
        return fd

    def _get_body_phash(self):
        return walk.get_body_phash_multi(walk.get_payloads(self._mime_multipart))

    def _hdoc(self):
        if self._hd:
            return self._hd

        hd = {}
        hd[fields.HEADERS_KEY] = self.headers
        hd[fields.DATE_KEY] = self.headers['Date']
        hd[fields.CONTENT_HASH_KEY] = self._get_chash()
        hd[fields.MSGID_KEY] = ''
        hd[fields.MULTIPART_KEY] = True
        hd[fields.SUBJECT_KEY] = self.headers.get('Subject')
        hd[fields.TYPE_KEY] = fields.TYPE_HEADERS_VAL
        hd[fields.BODY_KEY] = self._get_body_phash()
        hd[fields.PARTS_MAP_KEY] = walk.walk_msg_tree(walk.get_parts(self._mime_multipart), body_phash=self._get_body_phash())

        self._hd = hd
        return hd

    def _cdocs(self):
        return walk.get_raw_docs(self._mime_multipart, self._mime_multipart.walk())

    def to_mime_multipart(self):
        mime_multipart = MIMEMultipart()

        for header in ['To', 'Cc', 'Bcc']:
            if self.headers[header]:
                mime_multipart[header] = ", ".join(self.headers[header])

        if self.headers['subject']:
            mime_multipart['Subject'] = self.headers['Subject']

        mime_multipart['Date'] = self.headers['Date']
        mime_multipart.attach(MIMEText(self.body, 'plain'))
        return mime_multipart

    def to_smtp_format(self):
        mime_multipart = self.to_mime_multipart()
        mime_multipart['From'] = PixelatedMail.from_email_address
        return mime_multipart.as_string()


class PixelatedMail:

    def __init__(self, tag_service=TagService.get_instance()):
        self.tag_service = tag_service

    @staticmethod
    def from_soledad(fdoc, hdoc, bdoc, soledad_querier):
        mail = PixelatedMail()
        mail.bdoc = bdoc
        mail.fdoc = fdoc
        mail.hdoc = hdoc
        mail.querier = soledad_querier
        return mail

    @property
    def body(self):
        return self.bdoc.content['raw']

    @property
    def headers(self):
        _headers = ['From', 'Date', 'To', 'Subject', 'Cc', 'Bcc']
        _headers = {header: self.hdoc.content['headers'].get(header) for header in _headers}
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

    @property
    def uid(self):
        return self.fdoc.content['uid']

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

    def as_dict(self):
        statuses = [status.name for status in self.status]
        return {
            'header': {k.lower(): v for k, v in self.headers.items()},
            'ident': self.ident,
            'tags': list(self.tags),
            'status': statuses,
            'security_casing': self.security_casing,
            'body': self.body
        }


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

