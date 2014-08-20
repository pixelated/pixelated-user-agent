from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from common import *

def click_first_element_with_class(context, classname):
    elements = context.browser.find_elements_by_class_name(classname)
    elements[0].click()


@when('I select the tag \'{tag}\'')
def impl(context, tag):
    wait_for_user_alert_to_disapear(context)
    click_first_element_with_class(context, 'left-off-canvas-toggle')
    context.browser.execute_script("window.scrollBy(0, -200)")
    e = context.browser.find_element_by_xpath('//*[@id="tag-list"]/ul/li[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "%s")]' % tag)
    e.click()
