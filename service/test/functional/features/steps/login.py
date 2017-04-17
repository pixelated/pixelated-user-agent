#
# Copyright (c) 2016 ThoughtWorks, Inc.
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

from behave import given, when, then

from common import (
    fill_by_css_selector,
    find_element_by_css_selector)


@given('I am logged in Pixelated')
def login_user(context):
    login_page(context)
    enter_credentials(context)
    click_login(context)
    see_interstitial(context)
    _see_inbox(context)


@given(u'a user is accessing the login page')
@when(u'I open the login page')
def login_page(context):
    context.browser.get(context.login_url)


def _see_inbox(context):
    find_element_by_css_selector(context, '#compose', timeout=40)


@when(u'I enter username and password as credentials')
def enter_credentials(context):
    fill_by_css_selector(context, 'input[name="username"]', context.username)
    fill_by_css_selector(context, 'input[name="password"]', 'password')


@when(u'I click on the login button')
def click_login(context):
    find_element_by_css_selector(context, 'button[type="submit"]').click()


@then(u'I should see the fancy interstitial')
def see_interstitial(context):
    find_element_by_css_selector(context, 'section#hive-section')


@then(u'I should see the inbox')
def see_inbox(context):
    _see_inbox(context)


@then(u'I logout')
@when(u'I logout')
def click_logout(context):
    find_element_by_css_selector(context, '#logout-form div').click()


@then(u'I logout from the header')  # noqa
@when(u'I logout from the header')
def click_logout(context):
    find_element_by_css_selector(context, 'button[name="logout"]').click()


@when(u'I should see the login page')
@then(u'I should see the login page')
def see_login_page(context):
    find_element_by_css_selector(context, 'form#login_form')
