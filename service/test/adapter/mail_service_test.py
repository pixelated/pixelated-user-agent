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


class TestMailService(unittest.TestCase):

    @patch.object(MailService, '_append_mail_flags', return_value=None)
    @patch.object(MailService, '_remove_mail_flags', return_value=None)
    def test_custom_tags_get_created_if_not_exists(self, mockRemoveFlags, mockAppendFlags):
        MailService._open_leap_session = lambda self: None
        MailService.mailbox = PixelatedMailbox(test_helper.leap_mailbox(leap_flags=['\\Recent']))
        MailService.account = Mock(return_value=MagicMock())

        mailservice = MailService('username', 'password', 'leap_server')

        new_tags = ['test', 'inbox']
        updated_tags = mailservice.update_tags(6, new_tags)

        self.assertEquals(set([Tag('test'), Tag('inbox')]), set(updated_tags))
        # make sure that special tags are skipped when setting leap flags (eg.: tag_inbox)
        mockAppendFlags.assert_called_with(6, ['tag_test'])
        mockRemoveFlags.assert_called_with(6, [])
