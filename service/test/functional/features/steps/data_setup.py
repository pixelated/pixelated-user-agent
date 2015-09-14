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
from time import sleep
from uuid import uuid4
from test.support.integration import MailBuilder
from behave import given


@given('I have a mail in my inbox')
def add_mail_impl(context):
    subject = 'Hi! This the subject %s' % uuid4()

    input_mail = MailBuilder().with_subject(subject).build_input_mail()
    context.client.add_mail_to_inbox(input_mail)
    sleep(5) # we need to wait for the mail to be indexed (3 secs at least)

    context.last_subject = subject
