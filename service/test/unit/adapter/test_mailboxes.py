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
from twisted.trial import unittest
from pixelated.adapter.mailstore.leap_mailstore import LeapMail

from pixelated.adapter.services.mailboxes import Mailboxes
from mockito import mock, when, verify
from twisted.internet import defer
from mock import MagicMock


class PixelatedMailboxesTest(unittest.TestCase):

    def setUp(self):
        self.querier = mock()
        self.mail_store = mock()
        self.search_engine = mock()
        self.account = MagicMock()
        self.mailboxes = Mailboxes(self.account, self.mail_store, self.querier, self.search_engine)

    @defer.inlineCallbacks
    def test_move_to_inbox(self):
        when(self.mail_store).move_mail_to_mailbox(1, 'INBOX').thenReturn(defer.succeed(LeapMail('2', None, 'OTHER')))

        moved_mail = yield self.mailboxes.move_to_inbox(1)

        self.assertEqual('2', moved_mail.mail_id)
