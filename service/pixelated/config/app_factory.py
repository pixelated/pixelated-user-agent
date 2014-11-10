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
from twisted.internet import reactor
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.mail import InputMail
from pixelated.adapter.mail_sender import MailSender
from pixelated.adapter.mailboxes import Mailboxes
from pixelated.adapter.soledad_querier import SoledadQuerier
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.draft_service import DraftService
from pixelated.adapter.mailbox_indexer_listener import MailboxIndexerListener
import pixelated.bitmask_libraries.session as LeapSession
from pixelated.bitmask_libraries.leap_srp import LeapAuthException
from requests.exceptions import ConnectionError
from pixelated.controllers import *
from pixelated.adapter.tag_service import TagService
import os
import sys
from leap.common.events import (
    register,
    events_pb2 as proto
)
from twisted.web.iweb import IAccessLogFormatter
from twisted.web.server import Site
from zope.interface import provider


def init_index_and_remove_dupes(querier, search_engine, mail_service):
    def wrapper(*args, **kwargs):
        querier.remove_duplicates()
        search_engine.index_mails(mails=mail_service.all_mails(),
                                  callback=querier.mark_all_as_not_recent)

    return wrapper


def update_info_sync_and_index_partial(sync_info_controller, search_engine, mail_service):
    def wrapper(soledad_sync_status):
        sync_info_controller.set_sync_info(soledad_sync_status)
        search_engine.index_mails(mails=mail_service.all_mails())

    return wrapper


def _setup_routes(app, home_controller, mails_controller, tags_controller, features_controller, sync_info_controller, attachments_controller):
    # mails
    app.route('/mails', methods=['GET'])(mails_controller.mails)
    app.route('/mail/<mail_id>/read', methods=['POST'])(mails_controller.mark_mail_as_read)
    app.route('/mail/<mail_id>/unread', methods=['POST'])(mails_controller.mark_mail_as_unread)
    app.route('/mails/unread', methods=['POST'])(mails_controller.mark_many_mail_unread)
    app.route('/mails/read', methods=['POST'])(mails_controller.mark_many_mail_read)
    app.route('/mail/<mail_id>', methods=['GET'])(mails_controller.mail)
    app.route('/mail/<mail_id>', methods=['DELETE'])(mails_controller.delete_mail)
    app.route('/mails', methods=['DELETE'])(mails_controller.delete_mails)
    app.route('/mails', methods=['POST'])(mails_controller.send_mail)
    app.route('/mail/<mail_id>/tags', methods=['POST'])(mails_controller.mail_tags)
    app.route('/mails', methods=['PUT'])(mails_controller.update_draft)
    # tags
    app.route('/tags', methods=['GET'])(tags_controller.tags)
    # features
    app.route('/features', methods=['GET'])(features_controller.features)
    # sync info
    app.route('/sync_info', methods=['GET'])(sync_info_controller.sync_info)
    # attachments
    app.route('/attachment/<attachment_id>', methods=['GET'])(attachments_controller.attachment)
    # static
    app.route('/', methods=['GET'], branch=True)(home_controller.home)


def init_leap_session(app):
    try:
        leap_session = LeapSession.open(app.config['LEAP_USERNAME'],
                                        app.config['LEAP_PASSWORD'],
                                        app.config['LEAP_SERVER_NAME'])
    except ConnectionError, error:
        print("Can't connect to the requested provider")
        sys.exit(1)
    except LeapAuthException, e:
        print("Couldn't authenticate with the credentials provided %s" % e.message)
        sys.exit(1)
    return leap_session


def init_app(app):
    leap_session = init_leap_session(app)

    tag_service = TagService()
    search_engine = SearchEngine()
    pixelated_mail_sender = MailSender(leap_session.account_email())

    soledad_querier = SoledadQuerier(soledad=leap_session.account._soledad)
    pixelated_mailboxes = Mailboxes(leap_session.account, soledad_querier)
    draft_service = DraftService(pixelated_mailboxes)
    mail_service = MailService(pixelated_mailboxes, pixelated_mail_sender, tag_service, soledad_querier)

    MailboxIndexerListener.SEARCH_ENGINE = search_engine
    InputMail.FROM_EMAIL_ADDRESS = leap_session.account_email()

    home_controller = HomeController()
    features_controller = FeaturesController()
    mails_controller = MailsController(mail_service=mail_service,
                                       draft_service=draft_service,
                                       search_engine=search_engine)
    tags_controller = TagsController(search_engine=search_engine)
    sync_info_controller = SyncInfoController()
    attachments_controller = AttachmentsController(soledad_querier)

    register(signal=proto.SOLEDAD_SYNC_RECEIVE_STATUS,
             callback=update_info_sync_and_index_partial(sync_info_controller=sync_info_controller,
                                                         search_engine=search_engine,
                                                         mail_service=mail_service))
    register(signal=proto.SOLEDAD_DONE_DATA_SYNC,
             callback=init_index_and_remove_dupes(querier=soledad_querier,
                                                  search_engine=search_engine,
                                                  mail_service=mail_service))

    _setup_routes(app, home_controller, mails_controller, tags_controller, features_controller,
                  sync_info_controller, attachments_controller)


def create_app(app, bind_address, bind_port):
    print type(reactor.listenTCP)
    reactor.listenTCP(bind_port, Site(app.resource()), interface=bind_address)
    reactor.callWhenRunning(lambda: init_app(app))
    reactor.run()


def get_static_folder():
    static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
    # this is a workaround for packaging
    if not os.path.exists(static_folder):
        static_folder = os.path.abspath(
            os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", "web-ui", "app"))
    if not os.path.exists(static_folder):
        static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')
    return static_folder
