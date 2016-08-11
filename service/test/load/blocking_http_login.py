# Locustfile to run load tests for users with no emails, measuring how long the full login takes for pre-created users.
# Example usage:
#    locust -f /vagrant/service/test/load/blocking_http_login.py --no-web --num-request=1 --clients=1 --hatch-rate=1 --only-summary --host=http://localhost:3333
# The number of requests and number of clients should be the same number for this test

# Preconditions and behavior:
# - Ensure enough load test users are created. This should be one more than the number of requests/users specified
#   The format for users and password is "loadtestX" and "password_X" where X is the number of the user. The number starts on 1
#   An easy way to ensure users is to run 
#   python /vagrant/service/test/load/users.py --invite-code=bla-bla --number-11 --leap-provider=dev.pixelated-project.org
# - Before running the tests, you need to start the pixelated user agent and wait until it settles down. You should also
#   restart the agent before running another test, in order to ensure users are logged out and the measurements are independent.
# - It's recommended to truncate ~/MetricsTime before running a test, and moving it away somewhere after each test, in order
#   to get more specific timing information. Once you have more than one file, you can use the service/test/load/metrics/tabalute.rb
#   Ruby script to collate the information from the different metrics files, and find the areas of login that 
#   increase in an unreasonable way when number of users are increased.

import itertools
import os

import requests
from locust import HttpLocust, TaskSet, task
from locust.stats import RequestStats
from pixelated.resources.login_resource import LoginResource
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from users import User

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

user_number = itertools.count(1)

class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)

    @task(1)
    def index(self):
        self.client.cookies = requests.cookies.RequestsCookieJar()
        number = user_number.next()
        username = 'loadtest%d' % number
        password = 'password_%d' % number
        print("Logging in user: %s" % username)
        login_payload = {"username": username, "password": password}
        self.client.post("/%s" % LoginResource.BASE_URL,
                         login_payload,
                         timeout=3600000.0,
                         verify=False,
                         headers={
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-XSRF-TOKEN': "blablabla"
                         },
                         cookies={"XSRF-TOKEN": "blablabla"})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
