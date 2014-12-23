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
from pixelated.adapter.model.mail import PixelatedMail
from pixelated.adapter.soledad.soledad_facade_mixin import SoledadDbFacadeMixin


class SoledadWriterMixin(SoledadDbFacadeMixin, object):

    def mark_all_as_not_recent(self):
        for mailbox in ['INBOX', 'DRAFTS', 'SENT', 'TRASH']:
            rct = self.get_recent_by_mbox(mailbox)
            if len(rct) == 0:
                return
            rct = rct[0]
            rct.content['rct'] = []
            self.put_doc(rct)

    def save_mail(self, mail):
        self.put_doc(mail.fdoc)
        self._update_index([mail.fdoc])

    def create_mail(self, mail, mailbox_name):
        mbox = [m for m in self.get_all_mbox() if m.content['mbox'] == 'INBOX'][0]
        uid = mbox.content['lastuid'] + 1

        new_docs = [self.create_doc(doc) for doc in mail.get_for_save(next_uid=uid, mailbox=mailbox_name)]
        fdoc, hdoc, cdocs = new_docs[0], new_docs[1], new_docs[2:len(new_docs)]
        bdoc_index = None
        for i, val in enumerate(cdocs):
            if val.content['phash'] == hdoc.content['body']:
                bdoc_index = i
        bdoc = cdocs.pop(bdoc_index)

        mbox.content['lastuid'] = uid
        self.put_doc(mbox)

        self._update_index(new_docs)
        return self.mail(mail.ident) # PixelatedMail.from_soledad(fdoc, hdoc, bdoc, parts=None, soledad_querier=self)

    def remove_mail(self, mail):
        # FIX-ME: Must go through all the part_map phash to delete all the cdocs
        self.delete_doc(mail.fdoc)
        self.delete_doc(mail.hdoc)
        self.delete_doc(mail.bdoc)

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
