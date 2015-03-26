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
from common import *
from selenium.common.exceptions import NoSuchElementException
from time import sleep


def find_current_mail(context):
    return find_element_by_id(context, '%s' % context.current_mail_id)


def check_current_mail_is_visible(context):
    find_current_mail(context)


def open_current_mail(context):
    sleep(2)
    e = find_current_mail(context)
    e.click()


@then('I see that mail under the \'{tag}\' tag')
def impl(context, tag):
    context.execute_steps("when I select the tag '%s'" % tag)
    context.execute_steps(u'When I open the first mail in the mail list')


@when('I open that mail')
def impl(context):
    sleep(3)
    find_current_mail(context).click()


@when('I open the first mail in the mail list')
def impl(context):
    first_email = wait_until_elements_are_visible_by_locator(context, (By.XPATH, '//*[@id="mail-list"]//a'))[0]
    context.current_mail_id = 'mail-' + first_email.get_attribute('href').split('/')[-1]
    first_email.click()
    sleep(5)


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
    # wait_until_elements_are_visible_by_locator(context, (By.XPATH, '//*[@id="mail-list"]//a'))
    find_current_mail(context)


@given('I have mails')
def impl(context):
    emails = wait_until_elements_are_visible_by_locator(context, (By.XPATH, '//*[@id="mail-list"]//a'))
    assert len(emails) > 0


@when('I mark the first unread email as read')
def impl(context):
    emails = wait_until_elements_are_visible_by_locator(context, (By.XPATH, '//*[@id="mail-list"]//li'))

    for email in emails:
        if 'status-read' not in email.get_attribute('class'):
            email.find_element_by_tag_name('input').click()
            find_element_by_id(context, 'mark-selected-as-read').click()
            context.current_mail_id = email.get_attribute('id')
            break
    sleep(2)
    assert 'status-read' in context.browser.find_element_by_id(context.current_mail_id).get_attribute('class')


@when('I delete the email')
def impl(context):
    def last_email():
        return wait_until_elements_are_visible_by_locator(context, (By.XPATH, '//*[@id="mail-list"]//li'))[0]
    context.current_mail_id = last_email().get_attribute('id')
    last_email().find_element_by_tag_name('input').click()
    find_element_by_id(context, 'delete-selected').click()
    assert context.current_mail_id != find_elements_by_xpath(context, '//*[@id="mail-list"]//a')[0]


@when('I check all emails')
def impl(context):
    find_element_by_id(context, 'toggle-check-all-emails').click()


@when('I delete them permanently')
def impl(context):
    find_element_by_id(context, 'delete-selected').click()


@then('I should not see any email')
def impl(context):
    try:
        context.browser.find_element_by_xpath('//*[@id="mail-list"]//a')
    except NoSuchElementException:
        assert True
    except:
        assert False
