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
from leap.mail.adaptors.soledad import SoledadMailAdaptor
from twisted.internet import defer
from pixelated.adapter.mailstore import MailStore, underscore_uuid

from leap.mail.mail import Message
from pixelated.adapter.model.mail import Mail


class LeapMail(Mail):

    def __init__(self, mail_id, headers, tags=set(), body=None):
        self._mail_id = mail_id
        self.headers = headers
        self._body = body
        self.tags = tags

    @property
    def mail_id(self):
        return self._mail_id

    @property
    def body(self):
        return self._body

    def as_dict(self):
        return {
            'header': {k.lower(): v for k, v in self.headers.items()},
            'ident': self._mail_id,
            'tags': self.tags,
            'body': self._body
        }


class LeapMailStore(MailStore):
    __slots__ = ('soledad')

    def __init__(self, soledad):
        self.soledad = soledad

    @defer.inlineCallbacks
    def get_mail(self, mail_id, include_body=False):
        try:
            message = yield self._fetch_msg_from_soledad(mail_id)
            if not _is_empty_message(message):
                leap_mail = yield self._leap_message_to_leap_mail(mail_id, message, include_body)
            else:
                leap_mail = None

            defer.returnValue(leap_mail)
        except AttributeError, e:
            defer.returnValue(None)

    def get_mails(self, mail_ids):
        deferreds = []
        for mail_id in mail_ids:
            deferreds.append(self.get_mail(mail_id))

        return defer.gatherResults(deferreds, consumeErrors=True)

    @defer.inlineCallbacks
    def update_mail(self, mail):
        message = yield self._fetch_msg_from_soledad(mail.mail_id)
        message.get_wrapper().set_tags(tuple(mail.tags))
        message.get_wrapper().update(self.soledad)
        pass

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
    def add_mail(self, mailbox_name, raw_msg):
        mailbox = yield self._get_or_create_mailbox(mailbox_name)
        message = SoledadMailAdaptor().get_msg_from_string(Message, raw_msg)
        message.get_wrapper().set_mbox_uuid(mailbox.uuid)
        yield message.get_wrapper().create(self.soledad)

        # add behavious from insert_mdoc_id from mail.py
        mail = yield self._leap_message_to_leap_mail(message.get_wrapper().mdoc.doc_id, message, include_body=False)
        defer.returnValue(mail)

    @defer.inlineCallbacks
    def delete_mail(self, mail_id):
        message = yield self._fetch_msg_from_soledad(mail_id)
        yield message.get_wrapper().delete(self.soledad)

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
    def _leap_message_to_leap_mail(self, mail_id, message, include_body):
        if include_body:
            body = (yield message._wrapper.get_body(self.soledad)).raw
        else:
            body = None
        mail = LeapMail(mail_id, message.get_headers(), set(message.get_tags()), body=body)

        defer.returnValue(mail)

    def _get_or_create_mailbox(self, mailbox_name):
        return SoledadMailAdaptor().get_or_create_mbox(self.soledad, mailbox_name)

    def _fetch_msg_from_soledad(self, mail_id):
        return SoledadMailAdaptor().get_msg_from_mdoc_id(Message, self.soledad, mail_id)


def _is_empty_message(message):
    return (message is None) or (message.get_wrapper().mdoc.doc_id is None)


def _fdoc_id_to_mdoc_id(fdoc_id):
    return 'M' + fdoc_id[1:]
