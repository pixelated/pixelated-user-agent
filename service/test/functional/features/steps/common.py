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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from test.support.integration import MailBuilder


def wait_until_element_is_invisible_by_locator(context, locator_tuple, timeout=10):
    wait = WebDriverWait(context.browser, timeout)
    wait.until(EC.invisibility_of_element_located(locator_tuple))


def wait_until_element_is_deleted(context, locator_tuple, timeout=10):
    wait = WebDriverWait(context.browser, timeout)
    wait.until(lambda s: len(s.find_elements(locator_tuple[0], locator_tuple[1])) == 0)


def wait_for_user_alert_to_disapear(context, timeout=10):
    wait_until_element_is_invisible_by_locator(context, (By.ID, 'user-alerts'), timeout)


def wait_until_elements_are_visible_by_locator(context, locator_tuple, timeout=10):
    wait = WebDriverWait(context.browser, timeout)
    wait.until(EC.presence_of_all_elements_located(locator_tuple))
    return context.browser.find_elements(locator_tuple[0], locator_tuple[1])


def wait_until_elements_are_visible_by_xpath(context, locator_tuple, timeout=10):
    wait = WebDriverWait(context.browser, timeout)
    wait.until(EC.presence_of_all_elements_located(locator_tuple))
    return context.browser.find_elements(locator_tuple[0], locator_tuple[1])


def wait_until_element_is_visible_by_locator(context, locator_tuple, timeout=10):
    wait = WebDriverWait(context.browser, timeout)
    wait.until(EC.visibility_of_element_located(locator_tuple))
    return context.browser.find_element(locator_tuple[0], locator_tuple[1])


def fill_by_xpath(context, xpath, text):
    field = context.browser.find_element_by_xpath(xpath)
    field.send_keys(text)


def take_screenshot(context, filename):
    context.browser.save_screenshot(filename)


def dump_source_to(context, filename):
    with open(filename, 'w') as out:
        out.write(context.browser.page_source.encode('utf8'))


def page_has_css(context, css):
    try:
        find_element_by_css_selector(context, css)
        return True
    except TimeoutException:
        return False


def find_element_by_xpath(context, xpath):
    return wait_until_element_is_visible_by_locator(context, (By.XPATH, xpath))


def find_element_by_id(context, id):
    return wait_until_element_is_visible_by_locator(context, (By.ID, id))


def find_element_by_css_selector(context, css_selector):
    return wait_until_element_is_visible_by_locator(context, (By.CSS_SELECTOR, css_selector))


def find_elements_by_css_selector(context, css_selector):
    return wait_until_elements_are_visible_by_locator(context, (By.CSS_SELECTOR, css_selector))


def find_elements_by_xpath(context, xpath):
    return wait_until_elements_are_visible_by_xpath(context, (By.XPATH, xpath))


def find_element_containing_text(context, text, element_type='*'):
    return find_element_by_xpath(context, "//%s[contains(.,'%s')]" % (element_type, text))


def element_should_have_content(context, css_selector, content):
    e = find_element_by_css_selector(context, css_selector)
    assert e.text == content


def wait_until_button_is_visible(context, title, timeout=10):
    wait = WebDriverWait(context.browser, timeout)
    locator_tuple = (By.XPATH, ("//%s[contains(.,'%s')]" % ('button', title)))
    wait.until(EC.visibility_of_element_located(locator_tuple))


def click_button(context, title, element='button'):
    button = find_element_containing_text(context, title, element_type=element)
    button.click()


def mail_subject(context):
    e = find_element_by_css_selector(context, '#mail-view .subject')
    return e.text


def reply_subject(context):
    e = find_element_by_css_selector(context, '#reply-subject')
    return e.text


def get_console_log(context):
    logs = context.browser.get_log('browser')
    for entry in logs:
        msg = entry['message']
        if not (msg.startswith('x  off') or msg.startswith('<- on')):
            print entry['message']


def create_email(context):
    input_mail = MailBuilder().build_input_mail()
    context.client.add_mail_to_inbox(input_mail)
