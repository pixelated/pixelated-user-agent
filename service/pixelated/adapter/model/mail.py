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
import os
import re
import logging
from email import message_from_file
from email.mime.text import MIMEText
from email.header import Header
from email.MIMEMultipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from pycryptopp.hash import sha256
import leap.mail.walk as walk
from pixelated.adapter.model.status import Status
from pixelated.support import date


logger = logging.getLogger(__name__)


class Mail(object):
    @property
    def from_sender(self):
        return self.headers['From']

    @property
    def to(self):
        return self.headers['To']

    @property
    def cc(self):
        return self.headers['Cc']

    @property
    def bcc(self):
        return self.headers['Bcc']

    @property
    def subject(self):
        return self.headers['Subject']

    @property
    def date(self):
        return self.headers['Date']

    @property
    def status(self):
        return Status.from_flags(self.flags)

    @property
    def flags(self):
        return self.fdoc.content.get('flags')

    @property
    def mailbox_name(self):
        # FIXME mbox is no longer available, instead we now have mbox_uuid
        return self.fdoc.content.get('mbox', 'INBOX')

    def _encode_header_value_list(self, header_value_list):
        encoded_header_list = [self._encode_header_value(v) for v in header_value_list]
        return ', '.join(encoded_header_list)

    def _encode_header_value(self, header_value):
        if isinstance(header_value, unicode):
            return str(Header(header_value, 'utf-8'))
        return str(header_value)

    def _attach_body_mimetext_to(self, mime_multipart, body_to_use=None):
        body_to_use = body_to_use or self.body
        if isinstance(body_to_use, list):
            for part in body_to_use:
                mime_multipart.attach(MIMEText(part['raw'], part['content-type']))
        else:
            mime_multipart.attach(MIMEText(body_to_use, 'plain', self._charset()))

    @property
    def _mime_multipart(self):
        if self._mime:
            return self._mime
        mime = MIMEMultipart()
        for key, value in self.headers.items():
            if isinstance(value, list):
                mime[str(key)] = self._encode_header_value_list(value)
            else:
                mime[str(key)] = self._encode_header_value(value)

        body_to_use = getattr(self, 'body', None) or getattr(self, 'text_plain_body', None)
        self._attach_body_mimetext_to(mime, body_to_use)

        if self._attachments:
            for attachment in self._attachments:
                major, sub = attachment['content-type'].split('/')
                a = MIMENonMultipart(major, sub, Content_Disposition='attachment; filename=%s' % attachment['filename'])
                a.set_payload(attachment['raw'])
                mime.attach(a)

        self._mime = mime
        return mime

    def _charset(self):
        content_type = self.headers.get('content_type', {})
        if 'charset' in content_type:
            return self._parse_charset_header(content_type)
        return 'utf-8'

    def _parse_charset_header(self, charset_header, default_charset='utf-8'):
        try:
            return re.compile('.*charset=([a-zA-Z0-9-]+)', re.MULTILINE | re.DOTALL).match(charset_header).group(1)
        except:
            return default_charset

    @property
    def raw(self):
        return self._mime_multipart.as_string()

    def _get_chash(self):
        return sha256.SHA256(self.raw).hexdigest()


class InputMail(Mail):
    FROM_EMAIL_ADDRESS = None

    def __init__(self):
        self._raw_message = None
        self._fd = None
        self._hd = None
        self._bd = None
        self._chash = None
        self._mime = None
        self.headers = {}
        self.body = ''
        self._status = []
        self._attachments = []

    @property
    def ident(self):
        return self._get_chash()

    def _get_body_phash(self):
        return walk.get_body_phash(self._mime_multipart)

    def to_mime_multipart(self):
        mime_multipart = MIMEMultipart()

        for header in ['To', 'Cc', 'Bcc']:
            if self.headers.get(header):
                mime_multipart[header] = ", ".join(self.headers[header])

        if self.headers.get('Subject'):
            mime_multipart['Subject'] = self.headers['Subject']

        if self.headers.get('From'):
            mime_multipart['From'] = self.headers['From']

        mime_multipart['Date'] = self.headers['Date']
        self._attach_body_mimetext_to(mime_multipart)
        return mime_multipart

    def to_smtp_format(self):
        mime_multipart = self.to_mime_multipart()
        return mime_multipart.as_string()

    @staticmethod
    def delivery_error_template(delivery_address):
        return InputMail.from_dict({
            'body': "Mail undelivered for %s" % delivery_address,
            'header': {
                'bcc': [],
                'cc': [],
                'subject': "Mail undelivered for %s" % delivery_address
            }
        })

    @staticmethod
    # def from_dict(mail_dict, attachments):
    def from_dict(mail_dict):
        input_mail = InputMail()
        input_mail.headers = {key.capitalize(): value for key, value in mail_dict.get('header', {}).items()}

        input_mail.headers['Date'] = date.mail_date_now()
        input_mail.headers['From'] = InputMail.FROM_EMAIL_ADDRESS

        input_mail.body = mail_dict.get('body', '')
        input_mail.tags = set(mail_dict.get('tags', []))
        input_mail._status = set(mail_dict.get('status', []))
        input_mail._attachments = mail_dict.get('attachments', [])
        return input_mail

    @staticmethod
    def from_python_mail(mail):
        input_mail = InputMail()
        input_mail.headers = {unicode(key.capitalize()): unicode(value) for key, value in mail.items()}
        input_mail.headers[u'Date'] = unicode(date.mail_date_now())
        input_mail.headers[u'To'] = [u'']

        for payload in mail.get_payload():
            input_mail._mime_multipart.attach(payload)
            if payload.get_content_type() == 'text/plain':
                input_mail.body = unicode(payload.as_string())
        input_mail._mime = input_mail.to_mime_multipart()
        return input_mail


def welcome_mail():
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_path, '..', '..', 'assets', 'welcome.mail')) as mail_template_file:
        mail_template = message_from_file(mail_template_file)
    return InputMail.from_python_mail(mail_template)
