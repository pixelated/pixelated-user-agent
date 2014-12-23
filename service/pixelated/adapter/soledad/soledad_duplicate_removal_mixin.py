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
from pixelated.adapter.soledad.soledad_facade_mixin import SoledadDbFacadeMixin


class SoledadDuplicateRemovalMixin(SoledadDbFacadeMixin, object):

    def remove_duplicates(self):
        for mailbox in ['INBOX', 'DRAFTS', 'SENT', 'TRASH']:
            self._remove_dup_inboxes(mailbox)
            self._remove_dup_recent(mailbox)

    def _remove_many(self, docs):
        [self.delete_doc(doc) for doc in docs]

    def _remove_dup_inboxes(self, mailbox_name):
        mailboxes = self.get_mbox(mailbox_name)
        if len(mailboxes) == 0:
            return
        mailboxes_to_remove = sorted(mailboxes, key=lambda x: x.content['created'])[1:len(mailboxes)]
        self._remove_many(mailboxes_to_remove)

    def _remove_dup_recent(self, mailbox_name):
        rct = self.get_recent_by_mbox(mailbox_name)
        if len(rct) == 0:
            return
        rct_to_remove = sorted(rct, key=lambda x: len(x.content['rct']), reverse=True)[1:len(rct)]
        self._remove_many(rct_to_remove)
