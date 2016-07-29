import os
import time
from locust import HttpLocust, TaskSet, task
from pixelated.resources.login_resource import LoginResource

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from users import number_generator, User
from locust.stats import RequestStats


def noop(*arg, **kwargs):
    print "Stats reset prevented by monkey patch!"

RequestStats.reset_all = noop
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'unstable.pixelated-project.org')
INVITE_CODE = ''

user_number = number_generator()


class FirstTimeLogin(TaskSet):
    def __init__(self, *args, **kwargs):
        super(FirstTimeLogin, self).__init__(*args, **kwargs)
        self.cookies = {}

    def on_start(self):
        self.login()

    def login(self):
        index = user_number.next()
        load_test_user = User(index, LEAP_PROVIDER)
        username, password = load_test_user.get_or_create_user(INVITE_CODE)
        login_payload = {"username": username, "password": password}
        response = self.client.post("/%s" % LoginResource.BASE_URL, login_payload,
                                    timeout=1000000.0, verify=False, cookies=self.cookies)
        self._wait_for_interstitial(response)

    def _wait_for_interstitial(self, response):
        if response.status_code == 200:
            while not response.cookies.get('XSRF-TOKEN', ''):
                time.sleep(2)
                response = self.client.get("/", verify=False)
            self.cookies.update(response.cookies.get_dict())

    @task
    def index(self):
        self.client.get("/", cookies=self.cookies)


class WebsiteUser(HttpLocust):
    task_set = FirstTimeLogin
    min_wait = 1000
    max_wait = 5000
