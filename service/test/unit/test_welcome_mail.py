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

import os
import unittest
from mockito import verify, mock
from mockito.matchers import Matcher
from email import message_from_file
from pixelated.application import add_welcome_mail
from pixelated.adapter.model.mail import InputMail


class TestWelcomeMail(unittest.TestCase):

    def test_add_welcome_mail(self):
        mail_store = mock()
        input_mail = self._get_welcome_mail()

        add_welcome_mail(mail_store)
        capture = WelcomeMailCapture()

        verify(mail_store).add_mail('INBOX', capture)
        capture.assert_mail(input_mail.raw)

    def _get_welcome_mail(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path,
                               '..',
                               '..',
                               'pixelated',
                               'assets',
                               'welcome.mail')) as mail_template_file:
            mail_template = message_from_file(mail_template_file)

        return InputMail.from_python_mail(mail_template)


class WelcomeMailCapture(Matcher):

    def matches(self, arg):
        self.value = arg
        return True

    def assert_mail(self, mail):
        captured_mail = self._format(self.value)
        expected_mail = self._format(mail)
        assert captured_mail == expected_mail

    def _format(self, mail):
        splitter = '\n'
        arr = mail.split(splitter)
        arr = self._remove_variable_value(arr)

        return splitter.join(arr)

    def _remove_variable_value(self, arr):
        arr.pop(0)
        arr.pop(6)
        arr.pop(44)
        return arr
