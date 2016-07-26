import os
import json
from locust import HttpLocust, TaskSet, task
from pixelated.resources.login_resource import LoginResource

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from users import number, User

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'unstable.pixelated-project.org')
INVITE_CODE = ''


class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)
        self.cookies = {}

    def on_start(self):
        self.login()

    def login(self):
        index = number().next()
        load_test_user = User(index, LEAP_PROVIDER)
        username, password = load_test_user.get_or_create_user(INVITE_CODE)
        login_payload = {"username": username, "password": password}
        response = self.client.post("/%s" % LoginResource.BASE_URL,
                                    login_payload, verify=False, cookies=self.cookies)
        self.cookies.update(response.cookies.get_dict())
        self.username = username

    @task(1)
    def index(self):
        self.client.get("/", verify=False)

    @task(2)
    def mail_box(self):
        self.client.get("/mails?q=tag:'inbox'&p=1&w=25", verify=False)

    @task(3)
    def send_mail(self):
        payload = {
            "tags": ["drafts"],
            "body": "some text lorem ipsum" * 20,
            "attachments": [],
            "ident": "",
            "header": {
                "to": ["%s@%s" % (self.username, LEAP_PROVIDER)],
                "cc": [],
                "bcc": [],
                "subject": "load testing"}}

        self.cookies.update(self.client.get("/", verify=False).cookies.get_dict())
        with self.client.post('/mails', json=payload, catch_response=True, cookies=self.cookies,
                              headers=self._ajax_headers()) as email_response:
            if email_response.status_code == 201:
                email_id = json.loads(email_response.content)['ident']
                self.read_mail(email_id)
                self.delete_mail(email_id)
            else:
                email_response.failure('Error: email not Sent, status code: %s' % email_response.status_code)

    def _ajax_headers(self):
        return {'X-Requested-With': 'XMLHttpRequest', 'X-XSRF-TOKEN': self.cookies.get('XSRF-TOKEN', '')}

    def read_mail(self, ident):
        url = '/mail/%s' % ident
        self.client.get(url, cookies=self.cookies, headers=self._ajax_headers(), name='/read_mail')

    def delete_mail(self, ident):
        payload = {"idents": [ident]}
        self.client.post('/mails/delete', json=payload, cookies=self.cookies, verify=False, headers=self._ajax_headers())


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
