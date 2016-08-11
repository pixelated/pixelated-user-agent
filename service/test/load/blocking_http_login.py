import itertools
import os

import requests
from locust import HttpLocust, TaskSet, task
from locust.stats import RequestStats
from pixelated.resources.login_resource import LoginResource
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from users import User

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'dev.pixelated-project.org')
INVITE_CODE = 'bsuq-ahzc'

user_number = itertools.count(1)

class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)
        self.cookies = {}

    @task(1)
    def index(self):
        number = user_number.next()
        username = 'loadtestx_%d' % number
        password = 'password_%d' % number
        print "Logging in user: %s" % username
        login_payload = {"username": username, "password": password}
        self.cookies["XSRF-TOKEN"] = "blablabla"
        self.client.post("/%s" % LoginResource.BASE_URL,
                         login_payload,
                         timeout=3600000.0,
                         verify=False,
                         headers={
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-XSRF-TOKEN': "blablabla"
                        },
                        cookies=self.cookies)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
