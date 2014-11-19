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
from pixelated.adapter.mail import InputMail


class ReplyTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    def tearDown(self):
        SoledadTestBase.tearDown(self)

    def test_get_provides_template_for_reply_all(self):
        InputMail.FROM_EMAIL_ADDRESS = 'user@pixelated.org'
        mail = MailBuilder().with_subject('some subject').with_to_addresses(['user@pixelated.org', 'another@pixelated.org']).with_ident(1).build_input_mail()
        self.add_mail_to_inbox(mail)

        mails = self.get_mails_by_tag('inbox')
        self.assertNotIn('read', mails[0].status)

        response = self.reply_all_template(mail.ident)

        self.assertEquals(200, response['code'])
        self.assertEquals(['another@pixelated.org'], response['body']['header']['to'][0])
        self.assertEquals('Re: some subject', response['body']['header']['subject'])
