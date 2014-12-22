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


class DraftService(object):
    __slots__ = '_mailboxes'

    def __init__(self, mailboxes):
        self._mailboxes = mailboxes

    def create_draft(self, input_mail):
        self._drafts().add(input_mail)
        return input_mail

    def update_draft(self, ident, input_mail):
        new_mail = self.create_draft(input_mail)
        self._drafts().remove(ident)
        return new_mail

    def _drafts(self):
        return self._mailboxes.drafts()
