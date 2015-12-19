#
# Copyright (c) 2015 ThoughtWorks, Inc.
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
import base64
from email.header import decode_header
from email.utils import parseaddr
from uuid import uuid4

import re
from leap.mail.adaptors.soledad import SoledadMailAdaptor, ContentDocWrapper
from twisted.internet import defer
from pixelated.adapter.mailstore.body_parser import BodyParser
from pixelated.adapter.mailstore.mailstore import MailStore, underscore_uuid
from leap.mail.mail import Message
from pixelated.adapter.model.mail import Mail, InputMail

from pixelated.support.functional import to_unicode


class AttachmentInfo(object):
    def __init__(self, ident, name, encoding):
        self.ident = ident
        self.name = name
        self.encoding = encoding


class LeapMail(Mail):

    def __init__(self, mail_id, mailbox_name, headers=None, tags=set(), flags=set(), body=None, attachments=[]):
        self._mail_id = mail_id
        self._mailbox_name = mailbox_name
        self._headers = headers if headers is not None else {}
        self._body = to_unicode(body)
        self.tags = set(tags)   # TODO test that asserts copy
        self._flags = set(flags)  # TODO test that asserts copy
        self._attachments = attachments

    @property
    def headers(self):
        cpy = dict(self._headers)
        for name in set(self._headers.keys()).intersection(['To', 'Cc', 'Bcc']):
            cpy[name] = [address.strip() for address in (self._headers[name].split(',') if self._headers[name] else [])]

        return cpy

    @property
    def ident(self):
        return self._mail_id

    @property
    def mail_id(self):
        return self._mail_id

    @property
    def body(self):
        return self._body

    @property
    def flags(self):
        return self._flags

    @property
    def mailbox_name(self):
        return self._mailbox_name

    @property
    def security_casing(self):
        casing = dict(imprints=self._signature_information(), locks=[])
        if self._encrypted() == "decrypted":
            casing["locks"] = [{"state": "valid"}]
        return casing

    def _encrypted(self):
        return self.headers.get("X-Leap-Encryption", "false")

    def _signature_information(self):
        signature = self.headers.get("X-Leap-Signature", None)
        if signature is None or signature.startswith("could not verify"):
            return [{"state": "no_signature_information"}]
        else:
            if signature.startswith("valid"):
                return [{"state": "valid", "seal": {"validity": "valid"}}]
            else:
                return []

    @property
    def raw(self):
        result = u''
        for k, v in self._headers.items():
            content, encoding = decode_header(v)[0]
            if encoding:
                result += '%s: %s\n' % (k, unicode(content, encoding=encoding))
            else:
                result += '%s: %s\n' % (k, v)
        result += '\n'

        if self._body:
            result = result + self._body

        return result

    def _decoded_header_utf_8(self, header_value):
        if isinstance(header_value, list):
            return self.remove_duplicates([self._decoded_header_utf_8(v) for v in header_value])
        elif header_value is not None:
            def encode_chunk(content, encoding):
                return unicode(content.strip(), encoding=encoding or 'ascii', errors='ignore')

            try:
                encoded_chunks = [encode_chunk(content, encoding) for content, encoding in decode_header(header_value)]
                return ' '.join(encoded_chunks)  # decode_header strips whitespaces on all chunks, joining over ' ' is only a workaround, not a proper fix
            except UnicodeEncodeError:
                return unicode(header_value.encode('ascii', errors='ignore'))

    def as_dict(self):
        return {
            'header': {k.lower(): self._decoded_header_utf_8(v) for k, v in self.headers.items()},
            'ident': self._mail_id,
            'tags': self.tags,
            'status': list(self.status),
            'body': self._body,
            'security_casing': self.security_casing,
            'textPlainBody': self._body,
            'replying': self._replying_dict(),
            'mailbox': self._mailbox_name.lower(),
            'attachments': [{'ident': attachment.ident, 'name': attachment.name, 'encoding': attachment.encoding} for attachment in self._attachments]
        }

    def _replying_dict(self):
        result = {'single': None, 'all': {'to-field': [], 'cc-field': []}}

        sender_mail = self._decoded_header_utf_8(self.headers.get('Reply-To', self.headers.get('From')))
        # Issue #215: Fix for existing mails without any from address.
        if sender_mail is None:
            sender_mail = InputMail.FROM_EMAIL_ADDRESS

        recipients = self._reply_recipient('To')
        recipients = self._decoded_header_utf_8(recipients)
        recipients.append(sender_mail)
        recipients = self.remove_duplicates(recipients)
        ccs = self._decoded_header_utf_8(self._reply_recipient('Cc'))

        result['single'] = sender_mail
        result['all']['to-field'] = self._remove_me(recipients) if len(recipients) > 1 else recipients
        result['all']['cc-field'] = self._remove_me(ccs) if len(ccs) > 1 else ccs
        return result

    def _remove_me(self, recipients):
        return [recipient for recipient in recipients if not self._parsed_mail_matches(recipient, InputMail.FROM_EMAIL_ADDRESS)]

    def remove_duplicates(self, recipients):
        return list(set(recipients))

    def _reply_recipient(self, kind):
        recipients = self.headers.get(kind, [])
        if not recipients:
            recipients = []

        return recipients

    def _parsed_mail_matches(self, to_parse, expected):
        if InputMail.FROM_EMAIL_ADDRESS is None:
            return False
        return parseaddr(to_parse)[1] == expected

    @staticmethod
    def from_dict(mail_dict):
        # TODO: implement this method and also write tests for it
        headers = {key.capitalize(): value for key, value in mail_dict.get('header', {}).items()}
        headers['Date'] = date.mail_date_now()
        body = mail_dict.get('body', '')
        tags = set(mail_dict.get('tags', []))
        status = set(mail_dict.get('status', []))
        attachments = []

        # mail_id, mailbox_name, headers=None, tags=set(), flags=set(), body=None, attachments=[]
        return LeapMail(None, None, headers, tags, set(), body, attachments)


def _extract_filename(content_disposition):
    match = re.compile('.*name=\"(.*)\".*').search(content_disposition)
    filename = ''
    if match:
        filename = match.group(1)
    return filename


class LeapMailStore(MailStore):
    __slots__ = ('soledad')

    def __init__(self, soledad):
        self.soledad = soledad

    @defer.inlineCallbacks
    def get_mail(self, mail_id, include_body=False):
        message = yield self._fetch_msg_from_soledad(mail_id)
        if not _is_empty_message(message):
            leap_mail = yield self._leap_message_to_leap_mail(mail_id, message, include_body)
        else:
            leap_mail = None

        defer.returnValue(leap_mail)

    def get_mails(self, mail_ids):
        deferreds = []
        for mail_id in mail_ids:
            deferreds.append(self.get_mail(mail_id, include_body=True))

        return defer.gatherResults(deferreds, consumeErrors=True)

    @defer.inlineCallbacks
    def update_mail(self, mail):
        message = yield self._fetch_msg_from_soledad(mail.mail_id)
        message.get_wrapper().set_tags(tuple(mail.tags))
        message.get_wrapper().set_flags(tuple(mail.flags))
        yield self._update_mail(message)  # TODO assert this is yielded (otherwise asynchronous)

    @defer.inlineCallbacks
    def all_mails(self):
        mdocs = yield self.soledad.get_from_index('by-type', 'meta')

        mail_ids = map(lambda doc: doc.doc_id, mdocs)

        mails = yield self.get_mails(mail_ids)
        defer.returnValue(mails)

    @defer.inlineCallbacks
    def add_mailbox(self, mailbox_name):
        mailbox = yield self._get_or_create_mailbox(mailbox_name)
        defer.returnValue(mailbox)

    @defer.inlineCallbacks
    def get_mailbox_names(self):
        mbox_map = set((yield self._mailbox_uuid_to_name_map()).values())

        defer.returnValue(mbox_map.union({'INBOX'}))

    @defer.inlineCallbacks
    def _mailbox_uuid_to_name_map(self):
        map = {}
        mbox_docs = yield self.soledad.get_from_index('by-type', 'mbox')
        for doc in mbox_docs:
            map[underscore_uuid(doc.content.get('uuid'))] = doc.content.get('mbox')

        defer.returnValue(map)

    @defer.inlineCallbacks
    def add_mail(self, mailbox_name, raw_msg):
        mailbox = yield self._get_or_create_mailbox(mailbox_name)
        message = SoledadMailAdaptor().get_msg_from_string(Message, raw_msg)
        message.get_wrapper().set_mbox_uuid(mailbox.uuid)

        yield SoledadMailAdaptor().create_msg(self.soledad, message)

        # add behavious from insert_mdoc_id from mail.py
        mail = yield self._leap_message_to_leap_mail(message.get_wrapper().mdoc.doc_id, message, include_body=True)  # TODO test that asserts include_body
        defer.returnValue(mail)

    @defer.inlineCallbacks
    def delete_mail(self, mail_id):
        message = yield self._fetch_msg_from_soledad(mail_id)
        if message and message.get_wrapper().mdoc.doc_id:
            yield message.get_wrapper().delete(self.soledad)
            defer.returnValue(True)
        defer.returnValue(False)

    @defer.inlineCallbacks
    def get_mailbox_mail_ids(self, mailbox_name):
        mailbox = yield self._get_or_create_mailbox(mailbox_name)
        fdocs = yield self.soledad.get_from_index('by-type-and-mbox-uuid', 'flags', underscore_uuid(mailbox.uuid))

        mail_ids = map(lambda doc: _fdoc_id_to_mdoc_id(doc.doc_id), fdocs)

        defer.returnValue(mail_ids)

    @defer.inlineCallbacks
    def delete_mailbox(self, mailbox_name):
        mbx_wrapper = yield self._get_or_create_mailbox(mailbox_name)
        yield SoledadMailAdaptor().delete_mbox(self.soledad, mbx_wrapper)

    @defer.inlineCallbacks
    def copy_mail_to_mailbox(self, mail_id, mailbox_name):
        message = yield self._fetch_msg_from_soledad(mail_id, load_body=True)
        mailbox = yield self._get_or_create_mailbox(mailbox_name)
        copy_wrapper = yield message.get_wrapper().copy(self.soledad, mailbox.uuid)

        leap_message = Message(copy_wrapper)

        mail = yield self._leap_message_to_leap_mail(copy_wrapper.mdoc.doc_id, leap_message, include_body=False)

        defer.returnValue(mail)

    @defer.inlineCallbacks
    def move_mail_to_mailbox(self, mail_id, mailbox_name):
        mail_copy = yield self.copy_mail_to_mailbox(mail_id, mailbox_name)
        yield self.delete_mail(mail_id)
        defer.returnValue(mail_copy)

    def _update_mail(self, message):
        return message.get_wrapper().update(self.soledad)

    @defer.inlineCallbacks
    def _leap_message_to_leap_mail(self, mail_id, message, include_body):
        if include_body:
            # TODO use body from message if available
            body = yield self._raw_message_body(message)
        else:
            body = None

        # fetch mailbox name by mbox_uuid
        mbox_uuid = message.get_wrapper().fdoc.mbox_uuid
        mbox_name = yield self._mailbox_name_from_uuid(mbox_uuid)
        mail = LeapMail(mail_id, mbox_name, message.get_wrapper().hdoc.headers, set(message.get_tags()), set(message.get_flags()), body=body, attachments=self._extract_attachment_info_from(message))   # TODO assert flags are passed on

        defer.returnValue(mail)

    @defer.inlineCallbacks
    def _raw_message_body(self, message):
        content_doc = (yield message.get_wrapper().get_body(self.soledad))
        parser = BodyParser('', content_type='text/plain', content_transfer_encoding='UTF-8')
        # It fix the problem when leap doesn'r found body_phash and returns empty string
        if not isinstance(content_doc, str):
            parser = BodyParser(content_doc.raw, content_type=content_doc.content_type, content_transfer_encoding=content_doc.content_transfer_encoding)

        defer.returnValue(parser.parsed_content())

    @defer.inlineCallbacks
    def _mailbox_name_from_uuid(self, uuid):
        map = (yield self._mailbox_uuid_to_name_map())
        defer.returnValue(map.get(uuid, ''))

    @defer.inlineCallbacks
    def _get_or_create_mailbox(self, mailbox_name):
        mailbox_name_upper = mailbox_name.upper()
        mbx = yield SoledadMailAdaptor().get_or_create_mbox(self.soledad, mailbox_name_upper)
        if mbx.uuid is None:
            mbx.uuid = str(uuid4())
            yield mbx.update(self.soledad)
        defer.returnValue(mbx)

    def _fetch_msg_from_soledad(self, mail_id, load_body=False):
        return SoledadMailAdaptor().get_msg_from_mdoc_id(Message, self.soledad, mail_id, get_cdocs=load_body)

    @defer.inlineCallbacks
    def _dump_soledad(self):
        gen, docs = yield self.soledad.get_all_docs()
        for doc in docs:
            print '\n%s\n' % doc

    def _extract_attachment_info_from(self, message):
        wrapper = message.get_wrapper()
        part_maps = wrapper.hdoc.part_map
        return self._extract_part_map(part_maps)

    def _extract_part_map(self, part_maps):
        result = []

        for nr, part_map in part_maps.items():
            if 'headers' in part_map and 'phash' in part_map:
                headers = {header[0]: header[1] for header in part_map['headers']}
                phash = part_map['phash']
                if 'Content-Disposition' in headers:
                    disposition = headers['Content-Disposition']
                    if 'attachment' in disposition:
                        filename = _extract_filename(disposition)
                        encoding = headers.get('Content-Transfer-Encoding', None)
                        result.append(AttachmentInfo(phash, filename, encoding))
            if 'part_map' in part_map:
                result += self._extract_part_map(part_map['part_map'])

        return result


def _is_empty_message(message):
    return (message is None) or (message.get_wrapper().mdoc.doc_id is None)


def _fdoc_id_to_mdoc_id(fdoc_id):
    return 'M' + fdoc_id[1:]
