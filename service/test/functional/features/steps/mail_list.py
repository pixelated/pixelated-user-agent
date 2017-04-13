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

from behave import when, then, given
from selenium.common.exceptions import TimeoutException

from ..page_objects import InboxPage
from common import (
    ImplicitWait,
    find_element_by_id,
    find_element_by_css_selector,
    find_elements_by_css_selector,
    wait_for_condition,
    wait_for_loading_to_finish)


def find_current_mail(context):
    print('searching for mail [%s]' % context.current_mail_id)
    return find_element_by_id(context, '%s' % context.current_mail_id)


def check_current_mail_is_visible(context):
    find_current_mail(context)


def open_current_mail(context):
    e = find_current_mail(context)
    e.click()


@then('I see that mail under the \'{tag}\' tag')
def impl(context, tag):
    context.execute_steps("when I select the tag '%s'" % tag)
    context.execute_steps(u'When I open the first mail in the mail list')


@when('I open that mail')
def impl(context):
    find_current_mail(context).click()


@when('I open the first mail in the mail list')
def impl(context):
    InboxPage(context).open_first_mail_in_the_mail_list()


@when('I open the mail with the recovery code')
def impl(context):
    InboxPage(context).open_mail_with_the_recovery_code()


@when('I open the first mail in the \'{tag}\'')
def impl(context, tag):
    context.execute_steps(u"When I select the tag '%s'" % tag)
    context.execute_steps(u'When I open the first mail in the mail list')


@when('I open the mail I previously tagged')
def impl(context):
    open_current_mail(context)


@then('I see the mail I sent')
def impl(context):
    src = context.browser.page_source
    assert context.reply_subject in src


@then('the deleted mail is there')
def impl(context):
    InboxPage(context).get_mail_with_subject(context.last_subject)


@given('I have mails')
@then(u'I have mails')
def impl(context):
    emails = find_elements_by_css_selector(context, '.mail-list-entry', timeout=40)
    assert len(emails) > 0


@when('I mark the first unread email as read')
def impl(context):
    mail_id = find_element_by_css_selector(
        context, '.mail-list-entry:not(.status-read)').get_attribute('id')

    find_element_by_css_selector(context, '#%s input' % mail_id).click()
    find_element_by_id(context, 'mark-selected-as-read').click()

    find_element_by_css_selector(context, '#%s.status-read' % mail_id)


@when('I delete the email')
def impl(context):
    mail_id = find_element_by_css_selector(context, '.mail-list-entry').get_attribute('id')

    find_element_by_css_selector(context, '#%s input' % mail_id).click()
    find_element_by_id(context, 'delete-selected').click()

    _wait_for_mail_list_to_be_empty(context)


def _wait_for_mail_list_to_be_empty(context):
    wait_for_loading_to_finish(context)

    def mail_list_is_empty(_):
        with ImplicitWait(context, timeout=0.1):
            try:
                return 0 == len(context.browser.find_elements_by_css_selector('.mail-list-entry'))
            except TimeoutException:
                return False

    wait_for_condition(context, mail_list_is_empty)


@when('I check all emails')
def impl(context):
    find_element_by_id(context, 'toggle-check-all-emails').click()


@when('I delete them permanently')
def impl(context):
    find_element_by_id(context, 'delete-selected').click()


@then('I should not see any email')
def impl(context):
    _wait_for_mail_list_to_be_empty(context)


@then(u'I see the mail has the recovery code')
def step_impl(context):
    expected_body = 'Your code'
    context.execute_steps(u"Then I see that the body has '%s'" % expected_body)
