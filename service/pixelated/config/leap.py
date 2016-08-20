from __future__ import absolute_import
import logging
from twisted.internet import defer, threads
from leap.common.events import (server as events_server)
from leap.soledad.common.errors import InvalidAuthTokenError
from leap.auth import SRPAuth

from pixelated.config import credentials
from pixelated.config import leap_config
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.config.sessions import LeapSessionFactory

log = logging.getLogger(__name__)


def initialize_leap_provider(provider_hostname, provider_cert, provider_fingerprint, leap_home):
    LeapCertificate.set_cert_and_fingerprint(provider_cert,
                                             provider_fingerprint)
    leap_config.set_leap_home(leap_home)
    provider = LeapProvider(provider_hostname)
    provider.download_certificate()
    LeapCertificate(provider).setup_ca_bundle()

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
    try:
        yield leap_session.first_required_sync()
    except InvalidAuthTokenError:
        try:
            leap_session.close()
        except Exception, e:
            log.error(e)
        leap_session = LeapSessionFactory(provider).create(username, password, auth)
        yield leap_session.first_required_sync()

    defer.returnValue(leap_session)


@defer.inlineCallbacks
def initialize_leap_single_user(leap_provider_cert,
                                leap_provider_cert_fingerprint,
                                credentials_file,
                                leap_home):

    init_monkeypatches()
    events_server.ensure_server()

    provider, username, password = credentials.read(credentials_file)

    config, provider = initialize_leap_provider(provider, leap_provider_cert, leap_provider_cert_fingerprint, leap_home)

    try:
        auth = yield authenticate(provider, username, password)
    except SRPAuthenticationError:
        raise UnauthorizedLogin()

    leap_session = yield create_leap_session(provider, username, password, auth)

    defer.returnValue(leap_session)


def authenticate(provider, user, password):
    srp_auth = SRPAuth(provider.api_uri, provider.local_ca_crt)
    d = threads.deferToThread(srp_auth.authenticate, user, password)
    return d


def init_monkeypatches():
    import pixelated.extensions.requests_urllib3
