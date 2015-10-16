from __future__ import absolute_import
from pixelated.config import credentials
from leap.common.events import server as events_server, register, catalog as events
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.bitmask_libraries.session import LeapSessionFactory
from twisted.internet import defer


_CREATE_WELCOME_MAIL = False


def CREATE_WELCOME_MAIL():
    return _CREATE_WELCOME_MAIL


@defer.inlineCallbacks
def initialize_leap(leap_provider_cert,
                    leap_provider_cert_fingerprint,
                    credentials_file,
                    organization_mode,
                    leap_home,
                    initial_sync=True):
    init_monkeypatches()
    events_server.ensure_server()
    check_new_account()
    provider, username, password = credentials.read(organization_mode, credentials_file)
    LeapCertificate.set_cert_and_fingerprint(leap_provider_cert, leap_provider_cert_fingerprint)

    config = LeapConfig(leap_home=leap_home, start_background_jobs=True)
    provider = LeapProvider(provider, config)
    LeapCertificate(provider).setup_ca_bundle()
    leap_session = LeapSessionFactory(provider).create(username, password)
    logging.getLogger('gnupg').setLevel('WARN')

    if initial_sync:
        leap_session = yield leap_session.initial_sync()

    defer.returnValue(leap_session)


def init_monkeypatches():
    import pixelated.extensions.requests_urllib3


def mark_to_create_welcome_mail(_, x):
    global _CREATE_WELCOME_MAIL
    _CREATE_WELCOME_MAIL = True


def check_new_account():
    register(events.KEYMANAGER_FINISHED_KEY_GENERATION, mark_to_create_welcome_mail)
