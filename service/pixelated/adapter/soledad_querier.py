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
from pixelated.adapter.mail import PixelatedMail


class SoledadQuerier:

    def __init__(self, soledad):
        self.soledad = soledad

    def remove_inbox_duplicates(self):
        inboxes = [d for d in self.soledad.get_from_index('by-type', 'mbox') if d.content['mbox'] == 'INBOX']
        sorted(inboxes, key=lambda x: x.content['lastuid'], reverse=True)
        inboxes_to_remove = inboxes[1:len(inboxes)]
        [self.soledad.delete_doc(inbox) for inbox in inboxes_to_remove]

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

        fdocs_hdocs = [(f[0], self.soledad.get_from_index('by-type-and-contenthash', 'head', f[1])[0]) for f in fdocs_chash]
        fdocs_hdocs_phash = [(f[0], f[1], f[1].content.get('body')) for f in fdocs_hdocs]
        fdocs_hdocs_bdocs = [(f[0], f[1], self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', f[2])[0]) for f in fdocs_hdocs_phash]
        return [PixelatedMail.from_soledad(*raw_mail, soledad_querier=self) for raw_mail in fdocs_hdocs_bdocs]

    def save_mail(self, mail):
        # XXX update only what has to be updated
        self.soledad.put_doc(mail.fdoc)
        self.soledad.put_doc(mail.hdoc)
        self._update_index([mail.fdoc, mail.hdoc])

    def create_mail(self, mail, mailbox_name):
        uid = self._next_uid_for_mailbox(mailbox_name)
        new_docs = [self.soledad.create_doc(doc) for doc in mail._get_for_save(next_uid=uid, mailbox=mailbox_name)]
        self._update_index(new_docs)
        return self.mail(mail.ident)

    def mail(self, ident):
        fdoc = self.soledad.get_from_index('by-type-and-contenthash', 'flags', ident)[0]
        hdoc = self.soledad.get_from_index('by-type-and-contenthash', 'head', ident)[0]
        bdoc = self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', hdoc.content['body'])[0]

        return PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self)

    def mails(self, idents):
        fdocs_chash = [(self.soledad.get_from_index('by-type-and-contenthash', 'flags', ident), ident) for ident in idents]
        fdocs_chash = [(result[0], ident) for result, ident in fdocs_chash if result]
        return self._build_mails_from_fdocs(fdocs_chash)

    def remove_mail(self, mail):
        _mail = self.mail(mail.ident)
        # FIX-ME: Must go through all the part_map phash to delete all the cdocs
        self.soledad.delete_doc(_mail.fdoc)
        self.soledad.delete_doc(_mail.hdoc)
        self.soledad.delete_doc(_mail.bdoc)

    def idents_by_mailbox(self, mailbox_name):
        return set(doc.content['chash'] for doc in self.soledad.get_from_index('by-type-and-mbox-and-deleted', 'flags', mailbox_name, '0'))

    def _next_uid_for_mailbox(self, mailbox_name):
        mails = self.all_mails_by_mailbox(mailbox_name)
        mails.sort(key=lambda x: x.uid, reverse=True)
        if len(mails) == 0:
            return 1
        return mails[0].uid + 1

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
