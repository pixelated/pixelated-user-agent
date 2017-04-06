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

from ..page_objects import AccountRecoveryPage


@given(u'I am on the account recovery page')
def account_recovery_page(context):
    AccountRecoveryPage(context).visit()


@when(u'I submit admin recovery code')
def submit_admin_recovery_code(context):
    AccountRecoveryPage(context).submit_admin_recovery_code('1234')


@when(u'I submit user recovery code')
def submit_user_recovery_code(context):
    AccountRecoveryPage(context).submit_user_recovery_code('5678')


@when(u'I submit new password')
def submit_new_password(context):
    AccountRecoveryPage(context).submit_new_password('new test password', 'new test password')


@when(u'I click on the backup account link')
def go_to_backup_account(context):
    AccountRecoveryPage(context).go_to_backup_account()


@then(u'I see the backup account page')
def verify_backup_account_page(context):
    assert('/backup-account' in context.browser.current_url)
