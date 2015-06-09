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

from pixelated.resources.root_resource import RootResource
from pixelated.adapter.services.mail_service import MailService
from pixelated.adapter.model.mail import InputMail
from pixelated.adapter.services.mail_sender import MailSender
from pixelated.adapter.services.mailboxes import Mailboxes
from pixelated.adapter.soledad.soledad_querier import SoledadQuerier
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.services.draft_service import DraftService
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener


def init_app(leap_home, leap_session):
    keymanager = leap_session.nicknym.keymanager

    soledad_querier = SoledadQuerier(soledad=leap_session.account._soledad)

    search_engine = SearchEngine(soledad_querier, agent_home=leap_home)
    pixelated_mail_sender = MailSender(leap_session.account_email(), leap_session.smtp)

    pixelated_mailboxes = Mailboxes(leap_session.account, soledad_querier, search_engine)

    pixelated_mailboxes.add_welcome_mail_for_fresh_user()

    draft_service = DraftService(pixelated_mailboxes)
    mail_service = MailService(pixelated_mailboxes, pixelated_mail_sender, soledad_querier, search_engine)
    soledad_querier.remove_duplicates()
    search_engine.index_mails(mails=mail_service.all_mails(),
                              callback=soledad_querier.mark_all_as_not_recent)

    MailboxIndexerListener.SEARCH_ENGINE = search_engine
    InputMail.FROM_EMAIL_ADDRESS = leap_session.account_email()

    resource = RootResource()
    resource.initialize(keymanager, search_engine, mail_service, draft_service)

    return resource
