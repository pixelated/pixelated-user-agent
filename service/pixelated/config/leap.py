from __future__ import absolute_import
from leap.common.events import (server as events_server,
                                register, catalog as events)
from email import message_from_file
from pixelated.config import credentials
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.bitmask_libraries.session import LeapSessionFactory
from pixelated.adapter.model.mail import InputMail
from twisted.internet import defer
import os
import logging


fresh_account = False


@defer.inlineCallbacks
def initialize_leap(leap_provider_cert,
                    leap_provider_cert_fingerprint,
                    credentials_file,
                    organization_mode,
                    leap_home,
                    initial_sync=True):
    init_monkeypatches()
    events_server.ensure_server()
    register(events.KEYMANAGER_FINISHED_KEY_GENERATION,
             set_fresh_account)
    provider, username, password = credentials.read(organization_mode,
                                                    credentials_file)
    LeapCertificate.set_cert_and_fingerprint(leap_provider_cert,
                                             leap_provider_cert_fingerprint)

    config = LeapConfig(leap_home=leap_home, start_background_jobs=True)
    provider = LeapProvider(provider, config)
    LeapCertificate(provider).setup_ca_bundle()
    leap_session = LeapSessionFactory(provider).create(username, password)

    if initial_sync:
        leap_session = yield leap_session.initial_sync()

    global fresh_account
    if fresh_account:
        add_welcome_mail(leap_session.mail_store)

    defer.returnValue(leap_session)


def add_welcome_mail(mail_store):
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_path,
                           '..',
                           'assets',
                           'welcome.mail')) as mail_template_file:
        mail_template = message_from_file(mail_template_file)

    input_mail = InputMail.from_python_mail(mail_template)
    logging.getLogger('pixelated.config.leap').info('Adding the welcome mail')
    mail_store.add_mail('INBOX', input_mail.raw)


def init_monkeypatches():
    import pixelated.extensions.requests_urllib3


def set_fresh_account(_, x):
    global fresh_account
    fresh_account = True
