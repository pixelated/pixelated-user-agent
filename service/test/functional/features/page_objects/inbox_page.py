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
from steps.common import execute_ignoring_staleness


class InboxPage(BasePage):
    def __init__(self, context):
        super(InboxPage, self).__init__(context, context.inbox_url)

        self._locators = {
            'first_email': '.mail-list-entry__item',
            'read_sandbox': '#read-sandbox',
            'iframe_body': 'body',
        }

    def _get_first_mail(self):
        return self.find_element_by_css_selector(self._locators['first_email'])

    def get_mail_with_subject(self, subject):
        return self.find_element_by_xpath("//*[@class='mail-list-entry__item-subject' and contains(.,'%s')]" % subject)

    def open_first_mail_in_the_mail_list(self):
        # it seems page is often still loading so staleness exceptions happen often
        self.context.current_mail_id = 'mail-' + execute_ignoring_staleness(
            lambda: self._get_first_mail().get_attribute('href').split('/')[-1])
        execute_ignoring_staleness(lambda: self._get_first_mail().click())

    def open_mail_with_the_recovery_code(self):
        self.get_mail_with_subject('Recovery Code').click()

    def get_body_message(self):
        self.find_element_by_css_selector(self._locators['read_sandbox'])
        self.context.browser.switch_to_frame('read-sandbox')
        body_message = self.find_element_by_css_selector(self._locators['iframe_body']).text
        self.context.browser.switch_to_default_content()

        return body_message
