
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

from mailbox import Maildir
from twisted.internet import reactor, defer
from twisted.internet.threads import deferToThread
from pixelated.config.leap import initialize_leap
from pixelated.config import logger, arguments

from leap.mail.imap.fields import WithMsgFields


def initialize():
    args = arguments.parse_maintenance_args()

    logger.init(debug=args.debug)

    leap_session = initialize_leap(
        args.leap_provider_cert,
        args.leap_provider_cert_fingerprint,
        args.credentials_file,
        False,
        args.leap_home)

    execute_command = create_execute_command(args, leap_session)

    reactor.callWhenRunning(execute_command)
    reactor.run()


def create_execute_command(args, leap_session):
    def execute_command():

        def init_soledad():
            return leap_session

        def get_soledad_handle(leap_session):
            soledad = leap_session.soledad_session.soledad

            return leap_session, soledad

        def soledad_sync(args):
            leap_session, soledad = args

            soledad.sync()

            return args

        tearDown = defer.Deferred()

        prepare = deferToThread(init_soledad)
        prepare.addCallback(get_soledad_handle)
        prepare.addCallback(soledad_sync)
        add_command_callback(args, prepare, tearDown)
        tearDown.addCallback(soledad_sync)
        tearDown.addCallback(shutdown)
        tearDown.addErrback(shutdown_on_error)

    return execute_command


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


def add_mail_folder(account, maildir, folder_name, deferreds):
    if folder_name not in account.mailboxes:
        account.addMailbox(folder_name)

    mbx = account.getMailbox(folder_name)
    for mail in maildir:
        if is_keep_file(mail):
            continue

        flags = (WithMsgFields.RECENT_FLAG,) if mail.get_subdir() == 'new' else ()
        if 'S' in mail.get_flags():
            flags = (WithMsgFields.SEEN_FLAG,) + flags
        if 'R' in mail.get_flags():
            flags = (WithMsgFields.ANSWERED_FLAG,) + flags

        deferreds.append(mbx.addMessage(mail.as_string(), flags=flags, notify_on_disk=False))


@defer.inlineCallbacks
def load_mails(args, mail_paths):
    leap_session, soledad = args
    account = leap_session.account

    deferreds = []

    for path in mail_paths:
        maildir = Maildir(path, factory=None)
        add_mail_folder(account, maildir, 'INBOX', deferreds)
        for mail_folder_name in maildir.list_folders():
            mail_folder = maildir.get_folder(mail_folder_name)
            add_mail_folder(account, mail_folder, mail_folder_name, deferreds)

    yield defer.DeferredList(deferreds)
    defer.returnValue(args)


def flush_to_soledad(args, finalize):
    leap_session, soledad = args
    account = leap_session.account
    memstore = account._memstore
    permanent_store = memstore._permanent_store

    d = memstore.write_messages(permanent_store)

    def check_flushed(args):
        if memstore.is_writing:
            reactor.callLater(1, check_flushed, args)
        else:
            finalize.callback((leap_session, soledad))

    d.addCallback(check_flushed)

    return args


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
