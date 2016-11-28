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
import time

from behave import when, then
from selenium.webdriver.common.by import By

from common import (
    fill_by_css_selector,
    find_element_by_css_selector,
    wait_until_element_is_visible_by_locator)


@when(u'I open the login page')
def login_page(context):
    context.browser.get(context.multi_user_url + '/login')


@when(u'I enter {username} and {password} as credentials')
def enter_credentials(context, username, password):
    fill_by_css_selector(context, 'input#email', username)
    fill_by_css_selector(context, 'input#password', password)


@when(u'I click on the login button')
def click_login(context):
    login_button = wait_until_element_is_visible_by_locator(context, (By.CSS_SELECTOR, 'input[name="login"]'))
    login_button.click()


@then(u'I should see the fancy interstitial')
def step_impl(context):
    assert find_element_by_css_selector(context, 'section#hive-section')
    _wait_for_interstitial_to_reload()


def _wait_for_interstitial_to_reload():
    time.sleep(6)


@when(u'I logout')
def click_logout(context):
    logout_button = wait_until_element_is_visible_by_locator(context, (By.CSS_SELECTOR, 'ul#logout'))
    logout_button.click()


@then(u'I should see the login page')
def see_login_page(context):
    assert find_element_by_css_selector(context, 'form#login_form')
