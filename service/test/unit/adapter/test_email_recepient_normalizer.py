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
from pixelated.adapter.services.mail_sender import MailSender
from mockito import *
from test.support import test_helper


class PixelatedDuplicateEmailTest(unittest.TestCase):
    def setUp(self):
        self.mail_sender = MailSender(self, "random@gmail.com")

    def test_remove_duplicate_mail_recepients(self):
        mail_list = ['simba@gmail.com', 'simba@gmail.com', 'fabio@gmail.com']
        normalized_recepients = self.mail_sender.recepients_normalizer(mail_list)
        self.assertEquals(normalized_recepients, set(['simba@gmail.com', 'fabio@gmail.com']))

    def test_get_email_addresses(self):
        mail_list = ['simbarashe<simba@gmail.com>', 'vic@gmail.com', 'Fabio<fabio@gmail.com>', 'slick@gmail.com']
        selected_recepients = self.mail_sender.get_email_addresses(mail_list)
        self.assertEquals(selected_recepients, set(['simba@gmail.com', 'vic@gmail.com', 'fabio@gmail.com', 'slick@gmail.com']))

    def test_remove_duplicate_emails_with_routing_format(self):
        mail_list = ['simbarashe<simba@gmail.com>', 'simba<simba@gmail.com>', 'Fabio<fabio@gmail.com>', 'Fabinho<fabio@gmail.com>']
        selected_recepients = self.mail_sender.get_email_addresses(mail_list)
        self.assertEquals(selected_recepients, set(['simba@gmail.com', 'fabio@gmail.com']))
