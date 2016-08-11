import argparse
import os
from leap.auth import SRPAuth
from leap.exceptions import SRPAuthenticationError

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LEAP_PROVIDER = os.environ.get('LEAP_PROVIDER', 'unstable.pixelated-project.org')
LEAP_VERIFY_CERTIFICATE = os.environ.get('LEAP_VERIFY_CERTIFICATE', '~/.leap/ca.crt')


class User(object):
    def __init__(self, number, leap_provider=LEAP_PROVIDER):
        self._username = 'loadtest%d' % number
        self._password = 'password_%d' % number
        self._set_srp_auth(leap_provider)

    def _set_srp_auth(self, leap_provider):
        leap_api_server = 'https://api.%s:4430' % leap_provider
        leap_certificate = os.path.expanduser(LEAP_VERIFY_CERTIFICATE)
        self._srp_auth = SRPAuth(leap_api_server, leap_certificate)

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


def mass_register(number, invite_code):
    for index in xrange(1, number+1):
        User(index).register(invite_code)
        print 'done registering loadtest%d' % index


def ensure_leap_certificate(leap_provider, leap_certificate_home):
    certificate_home = os.path.expanduser(leap_certificate_home)
    if not os.path.exists(certificate_home):
        certificate = requests.get('https://%s/ca.crt' % leap_provider)
        with open(certificate_home, 'w') as certificate_file:
            certificate_file.write('%s' % certificate.content)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--number', '-n',  default=1, type=int, help='the number of user to be registered')
    parser.add_argument('--invite-code', '-i', default=None, help='invite code')
    parser.add_argument('--leap-provider', '-p', default=None, help='leap provider e.g. unstable.pix.org')
    parser.add_argument('--leap-ca-home', '-c', default=None, help='leap certificate home e.g. ~/.leap/ca.crt')
    return parser.parse_args()

if __name__ == '__main__':
    args = _parse_args()
    ensure_leap_certificate(args.leap_provider or LEAP_PROVIDER, args.leap_ca_home or LEAP_VERIFY_CERTIFICATE)
    mass_register(args.number, args.invite_code)
