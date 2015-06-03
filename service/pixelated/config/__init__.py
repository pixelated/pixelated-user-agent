#
# Copyright (c) 2014 ThoughtWorks, Inc.
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

from functools import partial
import sys

from pixelated.config import app_factory
from pixelated.config.args import parse_user_agent_args
from pixelated.config.loading_page import LoadingResource
from pixelated.config.register import register
from pixelated.config.logging_setup import init_logging
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
from twisted.internet import defer
from twisted.web.server import Site

from pixelated.config.initialize_leap import initialize_leap


@defer.inlineCallbacks
def start_user_agent(loading_app, host, port, sslkey, sslcert, leap_home, leap_session):
    yield loading_app.stopListening()

    app_factory.create_app(leap_home,
                           leap_session,
                           host,
                           port,
                           sslkey=sslkey,
                           sslcert=sslcert)


def initialize():
    args = parse_user_agent_args()
    init_logging(debug=args.debug)

    if args.register:
        register(*args.register)
        sys.exit(0)

    loading_app = reactor.listenTCP(args.port, Site(LoadingResource()), interface=args.host)

    deferred = deferToThread(
        lambda: initialize_leap(
            args.leap_provider_cert,
            args.leap_provider_cert_fingerprint,
            args.config_file,
            args.dispatcher,
            args.dispatcher_stdin,
            args.leap_home))

    deferred.addCallback(
        lambda leap_session: start_user_agent(
            loading_app,
            args.host,
            args.port,
            args.sslkey,
            args.sslcert,
            args.leap_home,
            leap_session))

    reactor.run()
