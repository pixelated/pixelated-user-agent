#
# Copyright (c) 2017 ThoughtWorks, Inc.
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


@given(u'I am on the account recovery page')
def account_recovery_page(context):
    context.browser.get(context.account_recovery_url)


@when(u'I submit admin recovery code')
def submit_admin_recovery_code(context):
    fill_by_css_selector(context, 'input[name="admin-code"]', '1234')
    find_element_by_css_selector(context, '.submit-button button[type="submit"]').click()


@when(u'I submit user recovery code')
def submit_user_recovery_code(context):
    fill_by_css_selector(context, 'input[name="user-code"]', '5678')
    find_element_by_css_selector(context, '.submit-button button[type="submit"]').click()


@when(u'I submit new password')
def submit_new_password(context):
    fill_by_css_selector(context, 'input[name="new-password"]', 'new test password')
    fill_by_css_selector(context, 'input[name="confirm-password"]', 'new test password')
    find_element_by_css_selector(context, '.submit-button button[type="submit"]').click()


@then(u'I see the backup account step')
def backup_account_step(context):
    find_element_by_css_selector(context, 'a[href="/backup-account"]', timeout=50)
