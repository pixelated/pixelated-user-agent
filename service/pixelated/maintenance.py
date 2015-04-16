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
import json
import argparse

from pixelated.config.app import App
from pixelated.config import app_factory
from pixelated.config.args import parser_add_default_arguments
from pixelated.config.config_ua import config_user_agent
from pixelated.config.dispatcher import config_dispatcher
from pixelated.config.events_server import init_events_server
from pixelated.config.loading_page import loading
from pixelated.config.register import register
from pixelated.config.logging_setup import init_logging
from pixelated.config.leap_cert import init_leap_cert
from pixelated.config.soledad import init_soledad_and_user_key
from twisted.internet import reactor, defer
from twisted.internet.threads import deferToThread

# monkey patching some specifics
import pixelated.support.ext_protobuf
import pixelated.support.ext_sqlcipher
import pixelated.support.ext_esmtp_sender_factory
import pixelated.support.ext_fetch
import pixelated.support.ext_keymanager_fetch_key
import pixelated.support.ext_requests_urllib3


def delete_all_mails(args):
    leap_session, soledad = args
    generation, docs = soledad.get_all_docs()

    for doc in docs:
        if doc.content.get('type', None) in ['head', 'cnt', 'flags']:
            soledad.delete_doc(doc)

    return args


def initialize():
    parser = argparse.ArgumentParser(description='pixelated maintenance')
    parser_add_default_arguments(parser)
    subparsers = parser.add_subparsers(help='commands')
    subparsers.add_parser('reset', help='reset account command')
    mails_parser = subparsers.add_parser('load-mails', help='load mails into account')
    mails_parser.add_argument('file', nargs='+', help='file(s) with mail data')

    args = parser.parse_args()
    app = App()

    init_logging(args)
    init_leap_cert(args)

    if args.dispatcher or args.dispatcher_stdin:
        config_dispatcher(app, args)
    else:
        config_user_agent(app, args)

    init_events_server()

    def execute_command():

        def init_soledad():
            return init_soledad_and_user_key(app, args.home)

        def get_soledad_handle(leap_session):
            soledad = leap_session.soledad_session.soledad

            return leap_session, soledad

        def soledad_sync(args):
            leap_session, soledad = args

            soledad.sync()

            return args

        d = deferToThread(init_soledad)
        d.addCallback(get_soledad_handle)
        d.addCallback(soledad_sync)
        d.addCallback(delete_all_mails)
        d.addCallback(soledad_sync)
        d.addCallback(shutdown)
        d.addErrback(shutdown_on_error)

    reactor.callWhenRunning(execute_command)
    reactor.run()


def shutdown(args):
    reactor.stop()


def shutdown_on_error(error):
    print error
    reactor.stop()

if __name__ == 'main':
    initialize()
