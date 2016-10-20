import re
from email.utils import parseaddr

class Authentication(object):

    def __init__(self, domain):
        self.domain = domain
        # self.token = token
        # self.uuid = uuid
        # self.session_id = session_id
        # self._user_attributes = user_attributes

    def authenticate(self, username, password):
        self.username = self.validate_username(username)
        self.srp_auth(username, password)

    def validate_username(self, username):
        if '@' not in username: return True
        extracted_username = self.extract_username(username)
        if self.username_with_domain(extracted_username) == username:
            return True
        else:
            return False

    def extract_username(self, username):
        return re.search('^([^@]+)@?.*$', username).group(1)

    def username_with_domain(self, username):
        return '%s@%s' % (username, self.domain)

    def is_admin(self):
        return self._user_attributes.get('is_admin', False)
