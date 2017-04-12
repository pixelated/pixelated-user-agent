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

from common import (
    element_should_have_content,
    fill_by_css_selector,
    find_element_by_css_selector)


def access_signup_page(context):
    context.browser.get(context.signup_url)


def create_user(context):
    context.browser.get(context.login_url)
    access_signup_page(context)
    enter_user_information(context)
    click_signup_button(context)
    see_user_control_panel(context)
    log_out(context)


def log_out(context):
    find_element_by_css_selector(context, 'a[href="/logout"]').click()


def enter_user_information(context):
    fill_by_css_selector(context, '#srp_username', context.username)
    fill_by_css_selector(context, '#srp_password', 'password')
    fill_by_css_selector(context, '#srp_password_confirmation', 'password')


def click_signup_button(context):
    find_element_by_css_selector(context, 'button[type=submit]').click()


def see_user_control_panel(context):
    element_should_have_content(context, 'h1', 'user control panel')
