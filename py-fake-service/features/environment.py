from selenium import webdriver


def before_feature(context, feature):
    #context.browser = webdriver.Firefox()
    context.browser = webdriver.PhantomJS()
    context.browser.set_window_size(1280, 1024)
    context.browser.implicitly_wait(5)
    context.browser.set_page_load_timeout(60) # wait for data
    context.browser.get('http://localhost:4567/')


def after_feature(context, feature):
    context.browser.quit()


def take_screenshot(context):
    context.browser.save_screenshot('/tmp/screenshot.jpeg')


def save_source(context):
    with open('/tmp/source.html', 'w') as out:
        out.write(context.browser.page_source.encode('utf8'))
