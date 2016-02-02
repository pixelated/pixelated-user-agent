import os
import json
import time
from random import randint

from leap.auth import SRPAuth
from leap.exceptions import SRPAuthenticationError
from locust import HttpLocust, TaskSet, task
from pixelated.resources.login_resource import LoginResource

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'dev.pixelated-project.org')
LEAP_SERVER_HOST = os.environ.get('LEAP_SERVER_HOST', 'https://api.%s:4430' % LEAP_PROVIDER)
LEAP_VERIFY_CERTIFICATE = os.environ.get('LEAP_VERIFY_CERTIFICATE', '~/.leap/ca.crt')
MAX_NUMBER_USER = os.environ.get('MAX_NUMBER_USER', 10000)
INVITES_FILENAME = os.environ.get('INVITES_FILENAME', '/tmp/invite_codes.txt')


def load_invite_from_number(number):
    with open(INVITES_FILENAME) as invites_file:
        lines = invites_file.readlines()
        return lines[number].strip()


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def _get_or_create_user(self, number):
        srp_auth = SRPAuth(LEAP_SERVER_HOST, os.path.expanduser(LEAP_VERIFY_CERTIFICATE))
        username, password = ('loadtest%d' % number), ('password_%d' % number)
#       username, password = 'loadtest123', 'asdfasdf'
        try:
            srp_auth.authenticate(username, password)
        except SRPAuthenticationError:
            srp_auth.register(username, password, load_invite_from_number(number))
        return username, password

    def login(self):
        number = randint(1, int(MAX_NUMBER_USER))
        username, password = self._get_or_create_user(number)
        self.client.post("/%s" % LoginResource.BASE_URL, {"username": username, "password": password})
        self.username = username
        time.sleep(5)

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def mail_box(self):
        self.client.get("/mails?q=tag:'inbox'&p=1&w=25")

    @task(3)
    def send_mail(self):
        payload = {"tags": ["drafts"], "body": "some text lorem ipsum", "attachments": [], "ident": "",
                   "header": {"to": ["%s@%s" % (self.username, LEAP_PROVIDER)], "cc": [], "bcc": [], "subject": "load testing"}}
        with self.client.post('/mails', json=payload, catch_response=True) as email_response:
            if email_response.status_code == 201:
                email_id = json.loads(email_response.content)['ident']
                print email_id
                self.delete_mail(email_id)
            else:
                email_response.failure('Error: email not Sent, status code: %s' % email_response.status_code)

    def delete_mail(self, ident):
        payload = {"idents": [ident]}
        self.client.post('/mails/delete', json=payload)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 15000
