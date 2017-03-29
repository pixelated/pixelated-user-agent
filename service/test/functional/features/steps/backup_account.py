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


@when(u'I go to the backup account page')
@given(u'I go to the backup account page')
def backup_account_page(context):
    context.browser.get(context.backup_account_url)


@when(u'I submit my backup account')
def submit_backup_email(context):
    fill_by_css_selector(context, 'input[name="email"]', 'test@test.com')
    find_element_by_css_selector(context, '.submit-button button[type="submit"]').click()


@then(u'I see the confirmation of this submission')
def confirmation_page(context):
    find_element_by_css_selector(context, '.confirmation-container', timeout=50)
