#
# Copyright (c) 2015 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

import os

from email import message_from_file
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import ssl
from OpenSSL import SSL
from OpenSSL import crypto

from pixelated.adapter.model.mail import InputMail
from pixelated.config import arguments
from pixelated.config.services import Services
from pixelated.config.leap import initialize_leap
from pixelated.config import logger
from pixelated.config.site import PixelatedSite
from pixelated.resources.root_resource import RootResource

from leap.common.events import (
    register,
    catalog as events
)


@defer.inlineCallbacks
def start_user_agent(root_resource, leap_home, leap_session):

    services = Services(leap_home, leap_session)
    yield services.setup(leap_home, leap_session)

    if leap_session.fresh_account:
        yield add_welcome_mail(leap_session.mail_store)

    root_resource.initialize(
        leap_session,
        services.keymanager,
        services.search_engine,
        services.mail_service,
        services.draft_service,
        services.feedback_service)

    # soledad needs lots of threads
    reactor.threadpool.adjustPoolsize(5, 15)


def _ssl_options(sslkey, sslcert):
    with open(sslkey) as keyfile:
        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, keyfile.read())
    with open(sslcert) as certfile:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, certfile.read())

    acceptable = ssl.AcceptableCiphers.fromOpenSSLCipherString(
        u'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:!RC4:HIGH:!MD5:!aNULL:!EDH')
    options = ssl.CertificateOptions(privateKey=pkey,
                                     certificate=cert,
                                     method=SSL.TLSv1_2_METHOD,
                                     acceptableCiphers=acceptable)
    return options


def initialize():
    args = arguments.parse_user_agent_args()
    logger.init(debug=args.debug)
    resource = RootResource()

    start_site(args, resource)

    deferred = initialize_leap(args.leap_provider_cert,
                               args.leap_provider_cert_fingerprint,
                               args.credentials_file,
                               args.organization_mode,
                               args.leap_home)

    deferred.addCallback(
        lambda leap_session: start_user_agent(
            resource,
            args.leap_home,
            leap_session))

    def _quit_on_error(failure):
        failure.printTraceback()
        reactor.stop()

    def _register_shutdown_on_token_expire(leap_session):
        register(events.SOLEDAD_INVALID_AUTH_TOKEN, lambda _: reactor.stop())
        return leap_session

    deferred.addCallback(_register_shutdown_on_token_expire)
    deferred.addErrback(_quit_on_error)

    reactor.run()


def start_site(config, resource):
    if config.sslkey and config.sslcert:
        reactor.listenSSL(config.port, PixelatedSite(resource), _ssl_options(config.sslkey, config.sslcert),
                          interface=config.host)
    else:
        reactor.listenTCP(config.port, PixelatedSite(resource), interface=config.host)


def add_welcome_mail(mail_store):
    current_path = os.path.dirname(os.path.abspath(__file__))
    welcome_mail = os.path.join(current_path, 'assets', 'welcome.mail')
    with open(welcome_mail) as mail_template_file:
        mail_template = message_from_file(mail_template_file)

    input_mail = InputMail.from_python_mail(mail_template)
    mail_store.add_mail('INBOX', input_mail.raw)
