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
from pixelated.config.args import parse as parse_args
from pixelated.config.events_server import init_events_server
from pixelated.config.loading_page import loading
from pixelated.config.register import register
from pixelated.config.logging_setup import init_logging
from pixelated.config.soledad import init_soledad_and_user_key
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
from pixelated.support.error_handler import error_handler

from pixelated.config.initialize_leap import initialize_leap


def initialize():
    args = parse_args()
    init_logging(debug=args.debug)

    app = initialize_leap(args.leap_provider_cert,
                          args.leap_provider_cert_fingerprint,
                          args.config,
                          args.dispatcher,
                          args.dispatcher_stdin)

    if args.register:
        register(*args.register)
        sys.exit(0)

    init_events_server()

    def load_app():
        # welcome to deferred hell. Or maybe you'll be welcomed later, who knows.
        loading_app = loading(args)

        def init_soledad():
            return init_soledad_and_user_key(app, args.home)

        def stop_loading_app(leap_session):
            d = loading_app.stopListening()
            d.addCallback(partial(start_user_agent_app, leap_session))

        def start_user_agent_app(leap_session, _):
            app_factory.create_app(app, args, leap_session)

        d = deferToThread(init_soledad)
        d.addCallback(stop_loading_app)
        d.addErrback(error_handler)

    reactor.callWhenRunning(load_app)
    reactor.run()
