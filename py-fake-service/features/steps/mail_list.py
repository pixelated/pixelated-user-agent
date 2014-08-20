import re
from behave import *
from common import *

def find_current_mail(context):
    return find_element_by_xpath(context, '//*[@id="mail-list"]/li[@id="mail-%s"]//a' % context.current_mail_id)


def check_current_mail_is_visible(context):
    find_current_mail(context)

def open_current_mail(context):
    e = find_current_mail(context)
    e.click()

@then('I see that mail under the \'{tag}\' tag')
def impl(context, tag):
    context.execute_steps("when I select the tag '%s'" % tag)
    check_current_mail_is_visible(context)

@when('I open that mail')
def impl(context):
	open_current_mail(context)

@when('I open the first mail in the mail list')
def impl(context):
    elements = context.browser.find_elements_by_xpath('//*[@id="mail-list"]//a')
    context.current_mail_id = elements[0].get_attribute('href').split('/')[-1]
    elements[0].click()

@when('I open the first mail in the \'{tag}\'')
def impl(context, tag):
    context.browser.execute_script('window.scrollBy(0, -200)')
    context.execute_steps(u"When I select the tag '%s'" % tag)
    context.execute_steps(u'When I open the first mail in the mail list')

@then('I open the mail I previously tagged')
def impl(context):
    open_current_mail(context)

@then('I see the mail I sent')
def impl(context):
    src = context.browser.page_source
    assert_that(src, contains_string(context.reply_subject))

@then('the deleted mail is there')
def impl(context):
    check_current_mail_is_visible(context)

