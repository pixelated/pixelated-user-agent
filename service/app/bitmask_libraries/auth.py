from .leap_srp import LeapSecureRemotePassword
from .certs import which_bundle

USE_PASSWORD = None


class LeapCredentials(object):
    def __init__(self, user_name, password, db_passphrase=USE_PASSWORD):
        self.user_name = user_name
        self.password = password
        self.db_passphrase = db_passphrase if db_passphrase is not None else password


class LeapAuthenticator(object):
    def __init__(self, provider):
        self._provider = provider

    def authenticate(self, credentials):
        config = self._provider.config
        srp = LeapSecureRemotePassword(ca_bundle=which_bundle(self._provider), timeout_in_s=config.timeout_in_s)
        srp_session = srp.authenticate(self._provider.api_uri, credentials.user_name, credentials.password)
        return srp_session
