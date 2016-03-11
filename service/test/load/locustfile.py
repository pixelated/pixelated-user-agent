import os
import json
from random import randint

from leap.auth import SRPAuth
from leap.exceptions import SRPAuthenticationError
from locust import HttpLocust, TaskSet, task
from pixelated.resources.login_resource import LoginResource

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'dev.pixelated-project.org')
LEAP_SERVER_HOST = os.environ.get(
    'LEAP_SERVER_HOST',
    'https://api.%s:4430' % LEAP_PROVIDER)
LEAP_VERIFY_CERTIFICATE = os.environ.get(
    'LEAP_VERIFY_CERTIFICATE',
    '~/.leap/ca.crt')
MAX_NUMBER_USER = os.environ.get('MAX_NUMBER_USER', 100)
INVITES_FILENAME = os.environ.get('INVITES_FILENAME', '/tmp/invite_codes.txt')
INVITES_ENABLED = os.environ.get('INVITES_ENABLED', 'true') == 'true'


def load_invite_from_number(number):
    with open(INVITES_FILENAME) as invites_file:
        lines = invites_file.readlines()
        return lines[number].strip()


class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)
        self.cookies = {}

    def on_start(self):
        self.login()

    def _get_or_create_user(self, number):
        srp_auth = SRPAuth(
            LEAP_SERVER_HOST,
            os.path.expanduser(LEAP_VERIFY_CERTIFICATE))
        username, password = ('loadtest%d' % number), ('password_%d' % number)
        try:
            srp_auth.authenticate(username, password)
        except SRPAuthenticationError:
            invite_code = None
            if INVITES_ENABLED:
                invite_code = load_invite_from_number(number)

            srp_auth.register(username, password, invite_code)
        return username, password

    def login(self):
        number = randint(1, int(MAX_NUMBER_USER))
        username, password = self._get_or_create_user(number)
        response = self.client.post(
            "/%s" % LoginResource.BASE_URL,
            {"username": username, "password": password})
        self.cookies.update(response.cookies.get_dict())
        resp = self.client.get("/")
        self.cookies.update(resp.cookies.get_dict())
        self.username = username

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def mail_box(self):
        self.client.get("/mails?q=tag:'inbox'&p=1&w=25")

    @task(3)
    def send_mail(self):
        payload = {
            "tags": ["drafts"],
            "body": "some text lorem ipsum",
            "attachments": [],
            "ident": "",
            "header": {
                "to": ["%s@%s" % (self.username, LEAP_PROVIDER)],
                "cc": [],
                "bcc": [],
                "subject": "load testing"}}

        self.cookies.update(
            self.client.get("/").cookies.get_dict())
        print(self.cookies)
        with self.client.post(
            '/mails',
            json=payload,
            catch_response=True,
            cookies=self.cookies,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'X-XSRF-TOKEN': self.cookies['XSRF-TOKEN']}) as email_response:
            if email_response.status_code == 201:
                email_id = json.loads(email_response.content)['ident']
                print email_id
                self.delete_mail(email_id)
            else:
                email_response.failure(
                    'Error: email not Sent, status code: %s' % (
                        email_response.status_code))

    def delete_mail(self, ident):
        payload = {"idents": [ident]}
        self.client.post(
            '/mails/delete',
            json=payload,
            cookies=self.cookies,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'X-XSRF-TOKEN': self.cookies['XSRF-TOKEN']})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000
