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
from email.parser import Parser
import os
from mockito import verify, mock
import pkg_resources
from twisted.trial.unittest import TestCase
from pixelated.adapter.mailstore.searchable_mailstore import SearchableMailStore
from pixelated.adapter.search import SearchEngine


class TestLeapMail(TestCase):
    def test_add_mail_delegates_to_mail_store_and_updates_index(self):
        mail = self._load_mail_from_file('mbox00000000')
        search_index = mock(mocked_obj=SearchEngine)
        delegate_mail_store = mock()
        store = SearchableMailStore(delegate_mail_store, search_index)

        store.add_mail('INBOX', mail)

        verify(search_index).index_mail(mail)
        verify(delegate_mail_store).add_mail('INBOX', mail)

    def _load_mail_from_file(self, mail_file):
        mailset_dir = pkg_resources.resource_filename('test.unit.fixtures', 'mailset')
        mail_file = os.path.join(mailset_dir, 'new', mail_file)
        with open(mail_file) as f:
            mail = Parser().parse(f)
        return mail
