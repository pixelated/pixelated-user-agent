import os
import json
import time

from locust import HttpLocust, TaskSet, task
from pixelated.resources.login_resource import LoginResource

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from users import User
import itertools
from locust.stats import RequestStats


def noop(*arg, **kwargs):
    print "Stats reset prevented by monkey patch!"

RequestStats.reset_all = noop
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'unstable.pixelated-project.org')
INVITE_CODE = 'abjs-axwp'

user_number = itertools.count(1)


class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)
        self.cookies = {}

    def on_start(self):
        self.login()

    def login(self):
        index = user_number.next()
        load_test_user = User(index, LEAP_PROVIDER)
        print '#USER ' + load_test_user._username
        username, password = load_test_user.get_or_create_user(INVITE_CODE)
        login_payload = {"username": username, "password": password}
        response = self.client.post("/%s" % LoginResource.BASE_URL,
                                    login_payload, verify=False, cookies=self.cookies)
        self._wait_for_interstitial(response)
        self.username = username

    def _wait_for_interstitial(self, response):
        while not response.cookies.get('XSRF-TOKEN', ''):
            time.sleep(1)
            response = self.client.get("/", verify=False)
        self.cookies.update(response.cookies.get_dict())

    @task(1)
    def index(self):
        self.client.get("/", verify=False)

    @task(1)
    def mail_box(self):
        self.client.get("/mails?q=tag:'inbox'&p=1&w=25", verify=False)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
