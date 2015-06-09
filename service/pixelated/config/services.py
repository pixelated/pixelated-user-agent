from pixelated.resources.root_resource import RootResource
from pixelated.adapter.services.mail_service import MailService
from pixelated.adapter.model.mail import InputMail
from pixelated.adapter.services.mail_sender import MailSender
from pixelated.adapter.services.mailboxes import Mailboxes
from pixelated.adapter.soledad.soledad_querier import SoledadQuerier
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.services.draft_service import DraftService
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener


class Services(object):

    def __init__(self, leap_home, leap_session):
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

        self.keymanager = keymanager
        self.search_engine = search_engine
        self.mail_service = mail_service
        self.draft_service = draft_service
