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
import os
import uuid

from crochet import setup, wait_for
from leap.common.events.server import ensure_server
from selenium import webdriver
from twisted.internet import defer
from twisted.logger import globalLogBeginner, textFileLogObserver, Logger

from pixelated.application import UserAgentMode
from pixelated.config.site import PixelatedSite
from pixelated.resources.features_resource import FeaturesResource
from test.support.integration import AppTestClient
from steps.common import DEFAULT_IMPLICIT_WAIT_TIMEOUT_IN_S

setup()

observers = [textFileLogObserver(open(os.devnull, 'w'))]

globalLogBeginner.beginLoggingTo(observers)

Logger('twisted')


@wait_for(timeout=5.0)
def start_app_test_client(client, mode):
    return client.start_client(mode=mode)


def before_all(context):
    userdata = context.config.userdata
    context.homepage_url = userdata.get('homepage_url', 'http://localhost:8889')
    context.multi_user_port = userdata.getint('multi_user_port', default=4568)
    context.multi_user_url = userdata.get('multi_user_url', 'http://localhost:4568')

    ensure_server()
    PixelatedSite.disable_csp_requests()
    client = AppTestClient()
    start_app_test_client(client, UserAgentMode(is_single_user=True))
    client.listenTCP(port=8889)
    FeaturesResource.DISABLED_FEATURES.append('autoRefresh')
    context.client = client

    multi_user_client = AppTestClient()
    start_app_test_client(multi_user_client, UserAgentMode(is_single_user=False))
    multi_user_client.listenTCP(port=context.multi_user_port)
    context.multi_user_client = multi_user_client


def after_all(context):
    context.client.stop()


def before_feature(context, feature):
    context.browser = webdriver.PhantomJS()
    context.browser.set_window_size(1280, 1024)
    context.browser.implicitly_wait(DEFAULT_IMPLICIT_WAIT_TIMEOUT_IN_S)
    context.browser.set_page_load_timeout(60)  # wait for data
    context.browser.get(context.homepage_url)


def after_step(context, step):
    if step.status == 'failed':
        id = str(uuid.uuid4())
        os.chdir("screenshots")
        context.browser.save_screenshot('failed ' + str(step.name) + '_' + id + ".png")
        save_source(context, 'failed ' + str(step.name) + '_' + id + ".html")
        os.chdir("../")


def after_feature(context, feature):
    context.browser.quit()

    cleanup_all_mails(context)
    context.last_mail = None


@wait_for(timeout=10.0)
def cleanup_all_mails(context):
    @defer.inlineCallbacks
    def _delete_all_mails():
        mails = yield context.client.mail_store.all_mails()
        for mail in mails:
            yield context.client.mail_store.delete_mail(mail.ident)

    return _delete_all_mails()


def save_source(context, filename='/tmp/source.html'):
    with open(filename, 'w') as out:
        out.write(context.browser.page_source.encode('utf8'))
