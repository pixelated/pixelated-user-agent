from selenium.webdriver.common.keys import Keys
from behave import *
from common import *
from hamcrest import *
from time import sleep

@when('I search for a mail with the words "{search_term}"')
def impl(context, search_term):
    search_field = find_element_by_css_selector(context, '#search-trigger input[type="search"]')
    search_field.send_keys(search_term)
    search_field.send_keys(Keys.ENTER)
    sleep(1)

@then('I see one or more mails in the search results')
def impl(context):
    lis = find_elements_by_css_selector(context, '#mail-list li')
    assert_that(len(lis), greater_than_or_equal_to(1))

