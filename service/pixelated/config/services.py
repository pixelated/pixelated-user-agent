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

        soledad_querier = SoledadQuerier(soledad=leap_session.account._soledad)

        self.search_engine = self.setup_search_engine(
            leap_home,
            soledad_querier)

        pixelated_mailboxes = Mailboxes(
            leap_session.account,
            soledad_querier,
            self.search_engine)

        self.mail_service = self.setup_mail_service(
            leap_session,
            soledad_querier,
            self.search_engine,
            pixelated_mailboxes)

        self.keymanager = self.setup_keymanager(leap_session)
        self.draft_service = self.setup_draft_service(pixelated_mailboxes)

        self.post_setup(soledad_querier, leap_session)

    def post_setup(self, soledad_querier, leap_session):
        self.search_engine.index_mails(
            mails=self.mail_service.all_mails(),
            callback=soledad_querier.mark_all_as_not_recent)
        soledad_querier.remove_duplicates()
        InputMail.FROM_EMAIL_ADDRESS = leap_session.account_email()

    def setup_keymanager(self, leap_session):
        return leap_session.nicknym.keymanager

    def setup_search_engine(self, leap_home, soledad_querier):
        key = soledad_querier.get_index_masterkey()
        search_engine = SearchEngine(key, agent_home=leap_home)
        MailboxIndexerListener.SEARCH_ENGINE = search_engine
        return search_engine

    def setup_mail_service(self, leap_session, soledad_querier, search_engine, pixelated_mailboxes):
        pixelated_mailboxes.add_welcome_mail_for_fresh_user()
        pixelated_mail_sender = MailSender(
            leap_session.account_email(),
            leap_session.smtp)
        return MailService(
            pixelated_mailboxes,
            pixelated_mail_sender,
            soledad_querier,
            search_engine)

    def setup_draft_service(self, pixelated_mailboxes):
        return DraftService(pixelated_mailboxes)
