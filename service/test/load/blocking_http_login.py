import itertools
import os

import requests
from locust import HttpLocust, TaskSet, task
from locust.stats import RequestStats
from pixelated.resources.login_resource import LoginResource
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from users import User


def noop(*arg, **kwargs):
    print "Stats reset prevented by monkey patch!"

RequestStats.reset_all = noop
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'unstable.pixelated-project.org')
INVITE_CODE = ''


user_number = itertools.count(600)


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
                                    login_payload, timeout=3600000.0,  verify=False, cookies=self.cookies)

    @task(1)
    def index(self):
        pass
        #self.client.get("/", verify=False)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 5000
