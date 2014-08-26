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

from pixelated.adapter.mail_service import MailService
from mock import Mock, MagicMock, patch
import test_helper
from pixelated.adapter.tag import Tag
from pixelated.adapter.pixelated_mailbox import PixelatedMailbox

class TestPixelatedMailbox(unittest.TestCase):

    @patch.object(MailService, 'set_flags', return_value=None)
    def test_retrieve_all_tags_from_mailbox(self, mockSetFlags):
        MailService._open_leap_session = lambda self: None
        leap_flags = ['\\Deleted', '\\Draft', '\\Recent', 'tag_custom', 'should_ignore_all_from_here', 'List']
        MailService.mailbox = PixelatedMailbox(test_helper.leap_mailbox(leap_flags=leap_flags))
        MailService.account = Mock(return_value=MagicMock())

        mailservice = MailService('username', 'password', 'leap_server')

        self.assertEquals(set([Tag('trash'), Tag('inbox'), Tag('drafts'), Tag('custom')]), mailservice.all_tags())
