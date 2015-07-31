
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

import logging
from mailbox import Maildir
from twisted.internet import reactor, defer
from twisted.internet.threads import deferToThread
from pixelated.config.leap import initialize_leap
from pixelated.config import logger, arguments

from leap.mail.constants import MessageFlags


def initialize():
    args = arguments.parse_maintenance_args()

    logger.init(debug=args.debug)

    @defer.inlineCallbacks
    def _run():
        leap_session = yield initialize_leap(
            args.leap_provider_cert,
            args.leap_provider_cert_fingerprint,
            args.credentials_file,
            organization_mode=False,
            leap_home=args.leap_home)

        execute_command(args, leap_session)

    reactor.callWhenRunning(_run)
    reactor.run()


def execute_command(args, leap_session):

    def init_soledad():
        return leap_session

    def get_soledad_handle(leap_session):
        soledad = leap_session.soledad_session.soledad

        return leap_session, soledad

    @defer.inlineCallbacks
    def soledad_sync(args):
        leap_session, soledad = args
        log = logging.getLogger('some logger')

        log.warn('Before sync')

        yield soledad.sync()

        log.warn('after sync')

        defer.returnValue(args)

    tearDown = defer.Deferred()

    prepare = deferToThread(init_soledad)
    prepare.addCallback(get_soledad_handle)
    prepare.addCallback(soledad_sync)
    add_command_callback(args, prepare, tearDown)
    tearDown.addCallback(soledad_sync)
    tearDown.addCallback(shutdown)
    tearDown.addErrback(shutdown_on_error)


def add_command_callback(args, prepareDeferred, finalizeDeferred):
    if args.command == 'reset':
        prepareDeferred.addCallback(delete_all_mails)
        prepareDeferred.addCallback(flush_to_soledad, finalizeDeferred)
    elif args.command == 'load-mails':
        prepareDeferred.addCallback(load_mails, args.file)
        prepareDeferred.addCallback(flush_to_soledad, finalizeDeferred)
    elif args.command == 'dump-soledad':
        prepareDeferred.addCallback(dump_soledad)
        prepareDeferred.chainDeferred(finalizeDeferred)
    elif args.command == 'sync':
        # nothing to do here, sync is already part of the chain
        prepareDeferred.chainDeferred(finalizeDeferred)
    else:
        print 'Unsupported command: %s' % args.command
        prepareDeferred.chainDeferred(finalizeDeferred)

    return finalizeDeferred


def delete_all_mails(args):
    leap_session, soledad = args
    generation, docs = soledad.get_all_docs()

    for doc in docs:
        if doc.content.get('type', None) in ['head', 'cnt', 'flags']:
            soledad.delete_doc(doc)

    return args


def is_keep_file(mail):
    return mail['subject'] is None


@defer.inlineCallbacks
def add_mail_folder(store, maildir, folder_name, deferreds):
    yield store.add_mailbox(folder_name)

    for mail in maildir:
        if is_keep_file(mail):
            continue

        flags = (MessageFlags.RECENT_FLAG,) if mail.get_subdir() == 'new' else ()
        if 'S' in mail.get_flags():
            flags = (MessageFlags.SEEN_FLAG,) + flags
        if 'R' in mail.get_flags():
            flags = (MessageFlags.ANSWERED_FLAG,) + flags

        deferreds.append(store.add_mail(folder_name, mail.as_string()))
        # FIXME support flags


@defer.inlineCallbacks
def load_mails(args, mail_paths):
    leap_session, soledad = args
    store = leap_session.mail_store

    deferreds = []

    for path in mail_paths:
        maildir = Maildir(path, factory=None)
        yield add_mail_folder(store, maildir, 'INBOX', deferreds)
        for mail_folder_name in maildir.list_folders():
            mail_folder = maildir.get_folder(mail_folder_name)
            yield add_mail_folder(store, mail_folder, mail_folder_name, deferreds)

    yield defer.gatherResults(deferreds, consumeErrors=True)

    defer.returnValue(args)


def flush_to_soledad(args, finalize):
    leap_session, soledad = args

    def after_sync():
        finalize.callback((leap_session, soledad))

    d = soledad.sync()
    d.addCallback(after_sync)

    return args


@defer.inlineCallbacks
def dump_soledad(args):
    leap_session, soledad = args

    generation, docs = yield soledad.get_all_docs()

    for doc in docs:
        print doc
        print '\n'

    defer.returnValue(args)


def shutdown(args):
    # time.sleep(30)
    reactor.stop()


def shutdown_on_error(error):
    print error
    shutdown(None)

if __name__ == '__main__':
    initialize()
