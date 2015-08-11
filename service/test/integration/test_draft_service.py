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

from test.support.integration import SoledadTestBase, MailBuilder


class DraftServiceTest(SoledadTestBase):

    @defer.inlineCallbacks
    def test_store_and_load_draft(self):
        input_mail = MailBuilder().with_body('some test text').build_input_mail()

        stored_draft = yield self.draft_service.create_draft(input_mail)

        draft = yield self.mail_store.get_mail(stored_draft.ident, include_body=True)

        self.assertEqual('some test text', draft.body)
