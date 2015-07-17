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
from twisted.internet import defer


class DraftService(object):
    __slots__ = '_mailboxes'

    def __init__(self, mailboxes):
        self._mailboxes = mailboxes

    @defer.inlineCallbacks
    def create_draft(self, input_mail):
        pixelated_mail = yield (yield self._mailboxes.drafts).add(input_mail)
        defer.returnValue(pixelated_mail)

    @defer.inlineCallbacks
    def update_draft(self, ident, input_mail):
        pixelated_mail = yield self.create_draft(input_mail)
        yield (yield self._mailboxes.drafts).remove(ident)
        defer.returnValue(pixelated_mail)
