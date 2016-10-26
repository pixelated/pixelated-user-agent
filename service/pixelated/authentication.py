import re
from pixelated.config.leap import authenticate
from leap.bitmask.bonafide._srp import SRPAuthError

from twisted.cred.error import UnauthorizedLogin
from twisted.internet.defer import inlineCallbacks


class Authenticator(object):
    def __init__(self, leap_provider):
        self._leap_provider = leap_provider
        self.domain = leap_provider.server_name

    @inlineCallbacks
    def authenticate(self, username, password):
        if self.validate_username(username):
            yield self._srp_auth(username, password)
        else:
            raise UnauthorizedLogin()

    @inlineCallbacks
    def _srp_auth(self, username, password):
        try:
            extracted_username = self.extract_username(username)
            auth = yield authenticate(self._leap_provider, extracted_username, password)
        except SRPAuthError:
            raise UnauthorizedLogin()

    def validate_username(self, username):
        if '@' not in username:
                return True
        extracted_username = self.extract_username(username)
        return self.username_with_domain(extracted_username) == username

    def extract_username(self, username):
        return re.search('^([^@]+)@?.*$', username).group(1)

    def username_with_domain(self, username):
        return '%s@%s' % (username, self.domain)
