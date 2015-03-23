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
import logging
import uuid

from test.support.dispatcher.proxy import Proxy
from test.support.integration import AppTestClient, MailBuilder
from selenium import webdriver

from pixelated.resources.features_resource import FeaturesResource


def before_all(context):
    logging.disable('INFO')
    client = AppTestClient()
    proxy = Proxy(proxy_port='8889', app_port='4567')
    FeaturesResource.DISABLED_FEATURES.append('autoRefresh')
    context.client = client
    context.call_to_terminate_proxy = proxy.run_on_a_thread()
    context.call_to_terminate = client.run_on_a_thread(logfile='/tmp/behave-tests.log')


def after_all(context):
    context.call_to_terminate()
    context.call_to_terminate_proxy()


def before_feature(context, feature):
    # context.browser = webdriver.Firefox()
    context.browser = webdriver.PhantomJS()
    context.browser.set_window_size(1280, 1024)
    context.browser.implicitly_wait(10)
    context.browser.set_page_load_timeout(60)  # wait for data
    context.browser.get('http://localhost:8889/')


def after_step(context, step):
    if step.status == 'failed':
        id = str(uuid.uuid4())
        context.browser.save_screenshot('failed '+str(step.name)+'_'+id+".png")
        save_source(context, 'failed '+str(step.name)+'_'+id+".html")


def after_feature(context, feature):
    context.browser.quit()


def save_source(context, filename='/tmp/source.html'):
    with open(filename, 'w') as out:
        out.write(context.browser.page_source.encode('utf8'))
