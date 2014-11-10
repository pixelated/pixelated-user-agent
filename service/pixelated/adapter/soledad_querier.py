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
import base64
import quopri

from cryptography.fernet import Fernet
from pixelated.adapter.mail import PixelatedMail
import re


class SoledadQuerier:

    def __init__(self, soledad):
        self.soledad = soledad

    @property
    def get_index_masterkey(self):
        index_key = self.soledad.get_from_index('by-type', 'index_key')
        if len(index_key) == 0:
            index_key = Fernet.generate_key()
            self.soledad.create_doc(dict(type='index_key', value=index_key))
            return index_key
        return str(index_key[0].content['value'])

    def _remove_many(self, docs):
        [self.soledad.delete_doc(doc) for doc in docs]

    def _remove_dup_inboxes(self, mailbox_name):
        mailboxes = self.soledad.get_from_index('by-type-and-mbox', 'mbox', mailbox_name)
        if len(mailboxes) == 0:
            return
        mailboxes_to_remove = sorted(mailboxes, key=lambda x: x.content['created'])[1:len(mailboxes)]
        self._remove_many(mailboxes_to_remove)

    def _remove_dup_recent(self, mailbox_name):
        rct = self.soledad.get_from_index('by-type-and-mbox', 'rct', mailbox_name)
        if len(rct) == 0:
            return
        rct_to_remove = sorted(rct, key=lambda x: len(x.content['rct']), reverse=True)[1:len(rct)]
        self._remove_many(rct_to_remove)

    def remove_duplicates(self):
        for mailbox in ['INBOX', 'DRAFTS', 'SENT', 'TRASH']:
            self._remove_dup_inboxes(mailbox)
            self._remove_dup_recent(mailbox)

    def mark_all_as_not_recent(self):
        for mailbox in ['INBOX', 'DRAFTS', 'SENT', 'TRASH']:
            rct = self.soledad.get_from_index('by-type-and-mbox', 'rct', mailbox)
            if len(rct) == 0:
                return
            rct = rct[0]
            rct.content['rct'] = []
            self.soledad.put_doc(rct)

    def all_mails(self):
        fdocs_chash = [(fdoc, fdoc.content['chash']) for fdoc in self.soledad.get_from_index('by-type', 'flags')]
        if len(fdocs_chash) == 0:
            return []
        return self._build_mails_from_fdocs(fdocs_chash)

    def all_mails_by_mailbox(self, mailbox_name):
        fdocs_chash = [(fdoc, fdoc.content['chash']) for fdoc in self.soledad.get_from_index('by-type-and-mbox', 'flags', mailbox_name)]
        return self._build_mails_from_fdocs(fdocs_chash)

    def _build_mails_from_fdocs(self, fdocs_chash):
        if len(fdocs_chash) == 0:
            return []

        fdocs_hdocs = []
        for fdoc, chash in fdocs_chash:
            hdoc = self.soledad.get_from_index('by-type-and-contenthash', 'head', chash)
            if len(hdoc) == 0:
                continue
            fdocs_hdocs.append((fdoc, hdoc[0]))

        fdocs_hdocs_bodyphash = [(f[0], f[1], f[1].content.get('body')) for f in fdocs_hdocs]
        fdocs_hdocs_bdocs = []
        for fdoc, hdoc, body_phash in fdocs_hdocs_bodyphash:
            bdoc = self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', body_phash)
            if len(bdoc) == 0:
                continue
            fdocs_hdocs_bdocs.append((fdoc, hdoc, bdoc[0]))

        return [PixelatedMail.from_soledad(*raw_mail, soledad_querier=self) for raw_mail in fdocs_hdocs_bdocs]

    def save_mail(self, mail):
        # XXX update only what has to be updated
        self.soledad.put_doc(mail.fdoc)
        self.soledad.put_doc(mail.hdoc)
        self._update_index([mail.fdoc, mail.hdoc])

    def create_mail(self, mail, mailbox_name):
        mbox = [m for m in self.soledad.get_from_index('by-type', 'mbox') if m.content['mbox'] == 'INBOX'][0]

        uid = mbox.content['lastuid'] + 1
        new_docs = [self.soledad.create_doc(doc) for doc in mail.get_for_save(next_uid=uid, mailbox=mailbox_name)]
        mbox.content['lastuid'] = uid

        self.soledad.put_doc(mbox)
        self._update_index(new_docs)

        return self.mail(mail.ident)

    def mail(self, ident):
        fdoc = self.soledad.get_from_index('by-type-and-contenthash', 'flags', ident)[0]
        hdoc = self.soledad.get_from_index('by-type-and-contenthash', 'head', ident)[0]
        parts = self._extract_parts(hdoc.content)
        bdoc = self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', hdoc.content['body'])[0]

        return PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self, parts=parts)

    def attachment(self, ident, encoding):
        bdoc = self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', ident)[0]
        return {'content': self._try_decode(bdoc.content['raw'], encoding),
                'content-type': bdoc.content['content-type']}

    def _try_decode(self, raw, encoding):
        encoding = encoding.lower()
        if encoding == 'base64':
            return base64.decodestring(raw)
        elif encoding == 'quoted-printable':
            return quopri.decodestring(raw)
        else:
            return str(raw)

    def mails(self, idents):
        fdocs_chash = [(self.soledad.get_from_index('by-type-and-contenthash', 'flags', ident), ident) for ident in idents]
        fdocs_chash = [(result[0], ident) for result, ident in fdocs_chash if result]
        return self._build_mails_from_fdocs(fdocs_chash)

    def _extract_parts(self, hdoc, parts=None):
        if not parts:
            parts = {'alternatives': [], 'attachments': []}

        if hdoc['multi']:
            for part_key in hdoc.get('part_map', {}).keys():
                self._extract_parts(hdoc['part_map'][part_key], parts)
        else:
            headers_dict = {elem[0]: elem[1] for elem in hdoc.get('headers', [])}
            if 'attachment' in headers_dict.get('Content-Disposition', ''):
                parts['attachments'].append(self._extract_attachment(hdoc, headers_dict))
            else:
                parts['alternatives'].append(self._extract_alternative(hdoc, headers_dict))
        return parts

    def _extract_alternative(self, hdoc, headers_dict):
        bdoc = self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', hdoc['phash'])[0]
        raw_content = bdoc.content['raw']
        return {'headers': headers_dict, 'content': raw_content}

    def _extract_attachment(self, hdoc, headers_dict):
        content_disposition = headers_dict['Content-Disposition']
        match = re.compile('.*name=\"(.*)\".*').search(content_disposition)
        filename = ''
        if match:
            filename = match.group(1)
        return {'headers': headers_dict, 'ident': hdoc['phash'], 'name': filename}

    def remove_mail(self, mail):
        _mail = self.mail(mail.ident)
        # FIX-ME: Must go through all the part_map phash to delete all the cdocs
        self.soledad.delete_doc(_mail.fdoc)
        self.soledad.delete_doc(_mail.hdoc)
        self.soledad.delete_doc(_mail.bdoc)

    def idents_by_mailbox(self, mailbox_name):
        return set(doc.content['chash'] for doc in self.soledad.get_from_index('by-type-and-mbox-and-deleted', 'flags', mailbox_name, '0'))

    def _update_index(self, docs):
        db = self.soledad._db

        indexed_fields = db._get_indexed_fields()
        if indexed_fields:
            # It is expected that len(indexed_fields) is shorter than
            # len(raw_doc)
            getters = [(field, db._parse_index_definition(field))
                       for field in indexed_fields]
            for doc in docs:
                db._update_indexes(doc.doc_id, doc.content, getters, db._db_handle)
