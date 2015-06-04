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
import sys

from twisted.internet import reactor
from pixelated.resources.root_resource import RootResource
from pixelated.adapter.services.mail_service import MailService
from pixelated.adapter.model.mail import InputMail
from pixelated.adapter.services.mail_sender import MailSender
from pixelated.adapter.services.mailboxes import Mailboxes
from pixelated.adapter.soledad.soledad_querier import SoledadQuerier
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.services.draft_service import DraftService
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener
import pixelated.bitmask_libraries.session as LeapSession
from requests.exceptions import ConnectionError
from leap.common.events import (
    register,
    unregister,
    events_pb2 as proto
)
from .welcome_mail import check_welcome_mail

INIT_INDEX_AND_REMOVE_DUPES_CALLBACK = 12346
CHECK_WELCOME_MAIL_CALLBACK = 12347


def init_index_and_remove_dupes(querier, search_engine, mail_service):
    def wrapper(*args, **kwargs):
        querier.remove_duplicates()
        search_engine.index_mails(mails=mail_service.all_mails(),
                                  callback=querier.mark_all_as_not_recent)
        unregister(proto.SOLEDAD_DONE_DATA_SYNC,
                   uid=INIT_INDEX_AND_REMOVE_DUPES_CALLBACK)

    return wrapper


def check_welcome_mail_wrapper(mailbox):
    def wrapper(*args, **kwargs):
        check_welcome_mail(mailbox)
        unregister(proto.SOLEDAD_DONE_DATA_SYNC,
                   uid=CHECK_WELCOME_MAIL_CALLBACK)
    return wrapper


def init_leap_session(app, leap_home):
    try:
        leap_session = LeapSession.open(app.config['LEAP_USERNAME'],
                                        app.config['LEAP_PASSWORD'],
                                        app.config['LEAP_SERVER_NAME'],
                                        leap_home=leap_home)
    except ConnectionError, error:
        print("Can't connect to the requested provider", error)
        reactor.stop()
        sys.exit(1)
    return leap_session


def init_app(leap_home, leap_session):
    leap_session.start_background_jobs()
    keymanager = leap_session.nicknym.keymanager

    soledad_querier = SoledadQuerier(soledad=leap_session.account._soledad)

    search_engine = SearchEngine(soledad_querier, agent_home=leap_home)
    pixelated_mail_sender = MailSender(leap_session.account_email(),
                                       lambda: leap_session.smtp.ensure_running())

    pixelated_mailboxes = Mailboxes(leap_session.account, soledad_querier, search_engine)
    draft_service = DraftService(pixelated_mailboxes)
    mail_service = MailService(pixelated_mailboxes, pixelated_mail_sender, soledad_querier, search_engine)

    MailboxIndexerListener.SEARCH_ENGINE = search_engine
    InputMail.FROM_EMAIL_ADDRESS = leap_session.account_email()

    resource = RootResource()
    resource.initialize(soledad_querier, keymanager, search_engine, mail_service, draft_service)

    register(signal=proto.SOLEDAD_DONE_DATA_SYNC,
             uid=INIT_INDEX_AND_REMOVE_DUPES_CALLBACK,
             callback=init_index_and_remove_dupes(querier=soledad_querier,
                                                  search_engine=search_engine,
                                                  mail_service=mail_service))

    register(signal=proto.SOLEDAD_DONE_DATA_SYNC,
             uid=CHECK_WELCOME_MAIL_CALLBACK,
             callback=check_welcome_mail_wrapper(pixelated_mailboxes.inbox()))

    return resource
