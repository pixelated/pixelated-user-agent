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
from email.mime.application import MIMEApplication
from time import sleep
from leap.mail.mail import Message
from common import *
from test.support.integration import MailBuilder
from behave import given
from crochet import wait_for
from uuid import uuid4
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText


@given(u'I have a mail with an attachment in my inbox')
def add_mail_with_attachment_impl(context):
    subject = 'Hi! This the subject %s' % uuid4()
    mail = build_mail_with_attachment(subject)
    load_mail_into_soledad(context, mail)
    context.last_subject = subject


def build_mail_with_attachment(subject):
    mail = MIMEMultipart()
    mail['Subject'] = subject
    mail.attach(MIMEText(u'a utf8 message', _charset='utf-8'))
    attachment = MIMEApplication('pretend to be binary attachment data')
    attachment.add_header('Content-Disposition', 'attachment', filename='filename.txt')
    mail.attach(attachment)

    return mail


@wait_for(timeout=10.0)
def load_mail_into_soledad(context, mail):
    return context.client.mail_store.add_mail('INBOX', mail.as_string())


@then(u'I see the mail has an attachment')
def step_impl(context):
    attachments_list = find_elements_by_css_selector(context, '.attachmentsArea li')
    assert len(attachments_list) == 1


@when(u'I find an attachment icon')
def find_icon(context):
    assert find_element_by_css_selector(context, '#attachment-button .fa.fa-paperclip')


@when(u'I try to upload a file bigger than 1MB')
def upload_big_file(context):
    base_dir = "test/functional/features/files/"
    fname = "image_over_1MB.png"
    fill_by_css_selector(context, '#fileupload', base_dir + fname)
    wait_until_element_is_visible_by_locator(context, (By.CSS_SELECTOR, '#upload-error-message'))


@then(u'I see an upload error message')
def show_upload_error_message(context):
    upload_error_message = find_elements_by_css_selector(context, '#upload-error-message')
    error_messages = [e.text for e in upload_error_message]
    assert "Upload failed. This file exceeds the 1MB limit." in error_messages


@when(u'I dismiss the error message')
def dismiss_error_message(context):
    dismiss_button = find_elements_by_css_selector(context, '#dismiss-button')
    assert len(dismiss_button) > 0
    for button in dismiss_button:
        button.click()


@then(u'It should not show the error message anymore')
def should_not_show_upload_error_message(context):
    upload_error_message_is_present = page_has_css(context, '#upload-error-message')
    assert not upload_error_message_is_present


@when(u'I upload a valid file')
def upload_attachment(context):
    base_dir = "test/functional/features/files/"
    fname = "upload_test_file.txt"
    fill_by_css_selector(context, '#fileupload', base_dir + fname)
    attachment_list_item = wait_until_element_is_visible_by_locator(context, (By.CSS_SELECTOR, '#attachment-list-item li a'))
    assert attachment_list_item.text == "%s (36.00 b)" % fname
