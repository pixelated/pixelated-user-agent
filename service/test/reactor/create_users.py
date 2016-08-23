# This script is used to mass register users
# ATTENTION: this script does not log
# the user in, so key creation will only
# happen on the first login
#
# You can run this with the following command:
# python create_users.py -n<number of users> -p<provider> -i<invite_code>

import argparse
import os
import tempfile
from leap.auth import SRPAuth
from leap.exceptions import SRPAuthenticationError

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class User(object):
    def __init__(self, number, provider, certificate):
        self._username = 'loadtest%d' % number
        self._password = 'password_%d' % number
        self._set_srp_auth(provider, certificate)

    def _set_srp_auth(self, leap_provider, certificate):
        leap_api_server = 'https://api.%s:4430' % leap_provider
        self._srp_auth = SRPAuth(leap_api_server, certificate)

    def get_or_create_user(self, invite_code=None):
        try:
            self.authenticate()
        except SRPAuthenticationError:
            self.register(invite_code)
        return self._username, self._password

    def authenticate(self):
        self._srp_auth.authenticate(self._username, self._password)

    def register(self, invite_code=None):
        self._srp_auth.register(self._username, self._password, invite_code)


def mass_register(number, invite_code, provider, certificate):
    for index in xrange(1, number + 1):
        User(index, provider, certificate).register(invite_code)
        print 'done registering loadtest%d' % index


def fetch_leap_certificate(leap_provider):
    _, certificate_path = tempfile.mkstemp()
    certificate = requests.get('https://%s/ca.crt' % leap_provider)
    with open(certificate_path, 'w') as cert:
        cert.write('%s' % certificate.content)
    return certificate_path


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--number', '-n', default=1, type=int, help='the number of user to be registered')
    parser.add_argument('--invite-code', '-i', default=None, help='invite code')
    parser.add_argument('--provider', '-p', default=None, help='leap provider e.g. unstable.pix.org')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    certificate_file = fetch_leap_certificate(args.provider)
    mass_register(args.number, args.invite_code, args.provider, certificate_file)
