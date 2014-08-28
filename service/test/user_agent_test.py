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
import pixelated.user_agent
from mock import Mock
import pixelated.adapter.pixelated_mail


class UserAgentTest(unittest.TestCase):

    def setUp(self):
        self.app = pixelated.user_agent.app.test_client()

    def test_send_mail_should_add_user_account(self):
        pixelated.user_agent.mail_service = Mock()
        pixelated.adapter.pixelated_mail.from_dict = lambda self: 'mail'

        self.app.post('/mails', data='{}', content_type="application/json")

        pixelated.user_agent.mail_service.send.assert_called_with('mail')
