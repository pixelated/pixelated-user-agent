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

import os
from functools import partial
import sys
import json
import argparse
import email

from os.path import join
from mailbox import mboxMessage
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

from leap.mail.imap.memorystore import MemoryStore
from leap.mail.imap.soledadstore import SoledadStore
from leap.common.events import register, unregister, events_pb2 as proto

# monkey patching some specifics
import pixelated.support.ext_protobuf
import pixelated.support.ext_sqlcipher
import pixelated.support.ext_esmtp_sender_factory
import pixelated.support.ext_fetch
import pixelated.support.ext_keymanager_fetch_key
import pixelated.support.ext_requests_urllib3


def initialize():
    args = parse_args()
    app = App()

    init_logging(args)
    init_leap_cert(args)

    if args.dispatcher or args.dispatcher_stdin:
        config_dispatcher(app, args)
    else:
        config_user_agent(app, args)

    init_events_server()
    execute_command = create_execute_command(args, app)

    reactor.callWhenRunning(execute_command)
    reactor.run()


def parse_args():
    parser = argparse.ArgumentParser(description='pixelated maintenance')
    parser_add_default_arguments(parser)
    subparsers = parser.add_subparsers(help='commands', dest='command')
    subparsers.add_parser('reset', help='reset account command')
    mails_parser = subparsers.add_parser('load-mails', help='load mails into account')
    mails_parser.add_argument('file', nargs='+', help='file(s) with mail data')

    subparsers.add_parser('dump-soledad', help='dump the soledad database')
    subparsers.add_parser('sync', help='sync the soledad database')

    return parser.parse_args()


def create_execute_command(args, app):
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
        add_command_callback(args, d)
        d.addCallback(soledad_sync)
        d.addCallback(shutdown)
        d.addErrback(shutdown_on_error)

    return execute_command


def add_command_callback(args, defer):
    if args.command == 'reset':
        defer.addCallback(delete_all_mails)
    elif args.command == 'load-mails':
        defer.addCallback(load_mails, args.file)
    elif args.command == 'dump-soledad':
        defer.addCallback(dump_soledad)
    elif args.command == 'sync':
        # nothing to do here, sync is already part of the chain
        pass
    else:
        print 'Unsupported command: %s' % args.command


def delete_all_mails(args):
    leap_session, soledad = args
    generation, docs = soledad.get_all_docs()

    for doc in docs:
        if doc.content.get('type', None) in ['head', 'cnt', 'flags']:
            soledad.delete_doc(doc)

    return args


@defer.inlineCallbacks
def load_mails(args, mail_paths):
    leap_session, soledad = args
    account = leap_session.account

    for path in mail_paths:
        print 'Loading mails from %s' % path
        for root, dirs, files in os.walk(path):
            mbx = account.getMailbox('INBOX')
            for f in files:
                with open(join(root, f), 'r') as fp:
                    m = email.message_from_file(fp)
                    flags = ("\\RECENT",)
                    r = yield mbx.addMessage(m.as_string(), flags=flags, notify_on_disk=False)
                    print 'Added message %s' % m.get('subject')
                    print m.as_string()

    defer.returnValue(args)
    return


def dump_soledad(args):
    leap_session, soledad = args

    generation, docs = soledad.get_all_docs()

    for doc in docs:
        print doc
        print '\n'

    return args


def shutdown(args):
    reactor.stop()


def shutdown_on_error(error):
    print error
    shutdown(None)

if __name__ == '__main__':
    initialize()
