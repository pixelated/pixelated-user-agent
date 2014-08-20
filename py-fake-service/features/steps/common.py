from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from hamcrest import *

def wait_until_element_is_invisible_by_locator(context, locator_tuple):
    wait = WebDriverWait(context.browser, 10)
    wait.until(EC.invisibility_of_element_located(locator_tuple))

def wait_for_user_alert_to_disapear(context):
    wait_until_element_is_invisible_by_locator(context, (By.ID, 'user-alerts'))

def wait_until_element_is_visible_by_locator(context, locator_tuple):
    wait = WebDriverWait(context.browser, 10)
    wait.until(EC.visibility_of_element_located(locator_tuple))


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
    except NoSuchElementException:
        return False

def find_element_by_xpath(context, xpath):
    return context.browser.find_element_by_xpath(xpath)

def find_element_by_css_selector(context, css_selector):
    return context.browser.find_element_by_css_selector(css_selector)

def find_elements_by_css_selector(context, css_selector):
    return context.browser.find_elements_by_css_selector(css_selector)

def find_element_containing_text(context, text, element_type='*'):
    return context.browser.find_element_by_xpath("//%s[contains(.,'%s')]" % (element_type, text))

def element_should_have_content(context, css_selector, content):
    e = find_element_by_css_selector(context, css_selector)
    assert_that(e.text, equal_to(content))

def wait_until_button_is_visible(context, title):
    wait = WebDriverWait(context.browser, 10)
    locator_tuple = (By.XPATH, ("//%s[contains(.,'%s')]" % ('button', title)))
    wait.until(EC.visibility_of_element_located(locator_tuple))

def click_button(context,  title):
    button = find_element_containing_text(context, title, element_type='button')
    button.click()

def mail_subject(context):
    e = find_element_by_css_selector(context, '#mail-view .subject')
    return e.text

def reply_subject(context):
    e = find_element_by_css_selector(context, '#reply-subject')
    return e.text
