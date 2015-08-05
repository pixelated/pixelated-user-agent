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
from mockito import verify, mock, when
import pkg_resources
from twisted.internet import defer
from twisted.trial.unittest import TestCase
from pixelated.adapter.mailstore.leap_mailstore import LeapMail
from pixelated.adapter.mailstore.searchable_mailstore import SearchableMailStore
from pixelated.adapter.search import SearchEngine


ANY_MAILBOX = 'INBOX'


class TestLeapMail(TestCase):

    def setUp(self):
        super(TestLeapMail, self).setUp()
        self.search_index = mock(mocked_obj=SearchEngine)
        self.delegate_mail_store = mock()
        self.store = SearchableMailStore(self.delegate_mail_store, self.search_index)

    @defer.inlineCallbacks
    def test_add_mail_delegates_to_mail_store_and_updates_index(self):
        mail = self._load_mail_from_file('mbox00000000')
        leap_mail = LeapMail('id', ANY_MAILBOX)
        when(self.delegate_mail_store).add_mail(ANY_MAILBOX, mail).thenReturn(defer.succeed(leap_mail))

        yield self.store.add_mail(ANY_MAILBOX, mail)

        verify(self.delegate_mail_store).add_mail(ANY_MAILBOX, mail)
        verify(self.search_index).index_mail(leap_mail)

    @defer.inlineCallbacks
    def test_add_mail_returns_stored_mail(self):
        mail = self._load_mail_from_file('mbox00000000')
        leap_mail = LeapMail('id', ANY_MAILBOX)
        when(self.delegate_mail_store).add_mail(ANY_MAILBOX, mail).thenReturn(defer.succeed(leap_mail))

        result = yield self.store.add_mail(ANY_MAILBOX, mail)

        self.assertEqual(leap_mail, result)

    def _load_mail_from_file(self, mail_file):
        mailset_dir = pkg_resources.resource_filename('test.unit.fixtures', 'mailset')
        mail_file = os.path.join(mailset_dir, 'new', mail_file)
        with open(mail_file) as f:
            mail = Parser().parse(f)
        return mail

