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

from base_page import BasePage


class AccountRecoveryPage(BasePage):
    def __init__(self, context):
        super(AccountRecoveryPage, self).__init__(context, context.account_recovery_url)

        self._locators = {
            'admin_form': '.account-recovery-form.admin-code',
            'admin_code': 'input[name="admin-code"]',
            'user_form': '.account-recovery-form.user-code',
            'user_code': 'input[name="user-code"]',
            'new_password_form': '.account-recovery-form.new-password',
            'new_password': 'input[name="new-password"]',
            'confirm_password': 'input[name="confirm-password"]',
            'submit_button': '.submit-button button[type="submit"]',
            'backup_account_link': 'a[href="/backup-account"]'
        }

    def submit_admin_recovery_code(self, admin_code):
        self.find_element_by_css_selector(self._locators['admin_form'])
        self.fill_by_css_selector(self._locators['admin_code'], admin_code)
        self.click_submit()

    def submit_user_recovery_code(self, user_code):
        self.find_element_by_css_selector(self._locators['user_form'])
        self.fill_by_css_selector(self._locators['user_code'], user_code)
        self.click_submit()

    def submit_new_password(self, new_password, confirm_password):
        self.find_element_by_css_selector(self._locators['new_password_form'])
        self.fill_by_css_selector(self._locators['new_password'], new_password)
        self.fill_by_css_selector(self._locators['confirm_password'], confirm_password)
        self.click_submit()

    def go_to_backup_account(self):
        self.find_element_by_css_selector(self._locators['backup_account_link']).click()

    def click_submit(self):
        submit_button = self.find_element_by_css_selector(self._locators['submit_button'])
        submit_button.click()
