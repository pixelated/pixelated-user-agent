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
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.status import Status
import test_helper
from pixelated.adapter.pixelated_mailbox import PixelatedMailbox
from mockito import *


class PixelatedMailboxTest(unittest.TestCase):
    def setUp(self):
        mail_one = test_helper.leap_mail(uid=0, mbox='SENT')
        leap_mailbox = test_helper.leap_mailbox(messages=[mail_one], mailbox_name='SENT')

        self.tag_service = mock()
        self.mailbox = PixelatedMailbox(leap_mailbox, self.tag_service)

    def test_mailbox_tag_is_added_when_recent_mail_arrives(self):
        recent_leap_mail = test_helper.leap_mail(uid=0, mbox='SPAM', flags=['\\Recent'])
        mailbox = PixelatedMailbox(test_helper.leap_mailbox(messages=[recent_leap_mail], mailbox_name='SPAM'))
        self.assertIn('spam', mailbox.mails()[0].tags)

    def test_mailbox_tag_is_ignored_for_non_recent_mail(self):
        recent_leap_mail = test_helper.leap_mail(uid=0, mbox='SPAM', flags=[])
        mailbox = PixelatedMailbox(test_helper.leap_mailbox(messages=[recent_leap_mail], mailbox_name='SPAM'))
        self.assertNotIn('spam', mailbox.mails()[0].tags)

    def test_add_message_to_mailbox_with_raw_message(self):
        mail = PixelatedMail.from_dict(test_helper.mail_dict())
        mail.raw_message = lambda: 'raw mail'

        leap_mailbox_messages = mock()
        self.mailbox.leap_mailbox.messages = leap_mailbox_messages

        self.mailbox._do_add_async.wrapped_function(self.mailbox, mail, use_smtp_format=False)

        verify(leap_mailbox_messages).add_msg('raw mail')

    def test_add_message_to_mailbox_with_smtp_format(self):
        mail = PixelatedMail.from_dict(test_helper.mail_dict())
        mail.to_smtp_format = lambda: 'smtp format mail'

        leap_mailbox_messages = mock()
        self.mailbox.leap_mailbox.messages = leap_mailbox_messages

        self.mailbox._do_add_async.wrapped_function(self.mailbox, mail, use_smtp_format=True)

        verify(leap_mailbox_messages).add_msg('smtp format mail')

    def test_remove_message_from_mailbox(self):
        mail = PixelatedMail.from_dict(test_helper.mail_dict())
        mail.raw_message = lambda: 'the mail in smtp format'

        mail.leap_mail = mock()
        self.mailbox.leap_mailbox = mock()

        self.mailbox.remove(mail)

        verify(mail.leap_mail).setFlags((Status.PixelatedStatus.DELETED,), 1)
        verify(self.mailbox.leap_mailbox).expunge()
