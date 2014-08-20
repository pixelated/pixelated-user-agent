from behave import given, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from common import *
from hamcrest import *


@given('I compose a message with')
def impl(context):
    take_screenshot(context, '/tmp/screenshot.jpeg')
    toggle = context.browser.find_element_by_id('compose-mails-trigger')
    toggle.click()

    for row in context.table:
        fill_by_xpath(context, '//*[@id="subject"]', row['subject'])
        fill_by_xpath(context, '//*[@id="text-box"]', row['body'])

@given("for the '{recipients_field}' field I type '{to_type}' and chose the first contact that shows")
def choose_impl(context, recipients_field, to_type):
    browser = context.browser
    browser.find_element_by_css_selector(
        '#recipients-to-area span input.tt-input'
        ).click()
    recipients_field = recipients_field.lower()
    css_selector = '#recipients-%s-area' % recipients_field
    recipients_element = browser.find_element_by_css_selector(css_selector)
    recipients_element.find_element_by_css_selector(
        '.tt-input'
        ).send_keys(to_type)
    wait_until_element_is_visible_by_locator(context, (By.CLASS_NAME, 'tt-dropdown-menu'))
    browser.find_element_by_css_selector('.tt-dropdown-menu div div').click()

@then("for the '{recipients_field}' field I type '{to_type}' and chose the first contact that shows")
def choose_impl(context, recipients_field, to_type):
    recipients_field = recipients_field.lower()
    browser = context.browser
    field = browser.find_element_by_css_selector(
        '#recipients-%s-area .tt-input' % recipients_field
        )
    field.send_keys(to_type)
    sleep(1)
    find_element_by_css_selector(context, '.tt-dropdown-menu div div').click()

@given('I save the draft')
def save_impl(context):
    context.browser.find_element_by_id('draft-button').click()


@when('I open the saved draft and send it')
def send_impl(context):
    context.execute_steps(u"when I select the tag 'drafts'")
    context.execute_steps(u"when I open the first mail in the mail list")
    assert_that(is_not(page_has_css(context, '#send-button[disabled]')))
    click_button(context, 'Send')
    element_should_have_content(context, '#user-alerts', 'Your message was sent!')

