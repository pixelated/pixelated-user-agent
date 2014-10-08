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
from test.support.integration_helper import MailBuilder, SoledadTestBase


class MarkAsReadTest(unittest.TestCase, SoledadTestBase):

    def setUp(self):
        self.setup_soledad()

    def tearDown(self):
        self.teardown_soledad()

    def test_mark_as_read(self):
        input_mail = MailBuilder().build_input_mail()
        self.add_mail_to_inbox(input_mail)

        mails = self.get_mails_by_tag('inbox')
        self.assertFalse('read' in mails[0].status)

        self.mark_as_read(input_mail.ident)

        mails = self.get_mails_by_tag('inbox')
        self.assertTrue('read' in mails[0].status)
