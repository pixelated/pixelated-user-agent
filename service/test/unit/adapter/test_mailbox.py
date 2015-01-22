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
import unittest

from pixelated.adapter.model.mail import PixelatedMail
from pixelated.adapter.services.mailbox import Mailbox
from mockito import *
from test.support import test_helper


class PixelatedMailboxTest(unittest.TestCase):
    def setUp(self):
        self.tag_service = mock()
        self.querier = mock()
        self.mailbox = Mailbox('INBOX', self.querier)

    def test_remove_message_from_mailbox(self):
        mail = PixelatedMail.from_soledad(*test_helper.leap_mail(), soledad_querier=self.querier)
        when(self.querier).mail(1).thenReturn(mail)

        self.mailbox.remove(1)

        verify(self.querier).remove_mail(mail)
