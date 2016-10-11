from __future__ import absolute_import
import logging
from collections import namedtuple
from twisted.cred.error import UnauthorizedLogin
from twisted.internet import defer, threads
from leap.common.events import (server as events_server)
from leap.soledad.common.errors import InvalidAuthTokenError
from leap.bitmask.bonafide._srp import SRPAuthError
from leap.bitmask.bonafide.session import Session
from leap.bitmask.bonafide.provider import Api
from pixelated.config import credentials
from pixelated.config import leap_config
from pixelated.config.authentication import Authentication
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.config.sessions import LeapSessionFactory

log = logging.getLogger(__name__)


Credentials = namedtuple('Credentials', 'username, password')


def initialize_leap_provider(provider_hostname, provider_cert, provider_fingerprint, leap_home):
    LeapCertificate.set_cert_and_fingerprint(provider_cert,
                                             provider_fingerprint)
    leap_config.set_leap_home(leap_home)
    provider = LeapProvider(provider_hostname)
    provider.setup_ca()
    provider.download_settings()
    return provider


@defer.inlineCallbacks
def initialize_leap_multi_user(provider_hostname,
                               leap_provider_cert,
                               leap_provider_cert_fingerprint,
                               credentials_file,
                               leap_home):

    config, provider = initialize_leap_provider(provider_hostname, leap_provider_cert, leap_provider_cert_fingerprint, leap_home)

    defer.returnValue((config, provider))


@defer.inlineCallbacks
def create_leap_session(provider, username, password, auth=None):
    leap_session = yield LeapSessionFactory(provider).create(username, password, auth)
    defer.returnValue(leap_session)


@defer.inlineCallbacks
def initialize_leap_single_user(leap_provider_cert,
                                leap_provider_cert_fingerprint,
                                credentials_file,
                                leap_home):

    init_monkeypatches()
    events_server.ensure_server()

    provider, username, password = credentials.read(credentials_file)

    provider = initialize_leap_provider(provider, leap_provider_cert, leap_provider_cert_fingerprint, leap_home)

    try:
        auth = yield authenticate(provider, username, password)
    except SRPAuthError:
        raise UnauthorizedLogin()

    leap_session = yield create_leap_session(provider, username, password, auth)

    defer.returnValue(leap_session)


@defer.inlineCallbacks
def authenticate(provider, user, password):
    srp_provider = Api(provider.api_uri)
    credentials = Credentials(user, password)
    srp_auth = Session(credentials, srp_provider, provider.local_ca_crt)
    yield srp_auth.authenticate()
    defer.returnValue(Authentication(user, srp_auth.token, srp_auth.uuid, 'session_id', {'is_admin': False}))


def init_monkeypatches():
    import pixelated.extensions.requests_urllib3
