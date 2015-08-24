from pixelated.adapter.mailstore.searchable_mailstore import SearchableMailStore
from pixelated.adapter.services.mail_service import MailService
from pixelated.adapter.model.mail import InputMail
from pixelated.adapter.services.mail_sender import MailSender
from pixelated.adapter.services.mailboxes import Mailboxes
from pixelated.adapter.soledad.soledad_querier import SoledadQuerier
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.services.draft_service import DraftService
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener
from twisted.internet import defer


class Services(object):

    def __init__(self, leap_home, leap_session):
        pass

    @defer.inlineCallbacks
    def setup(self, leap_home, leap_session):

        soledad_querier = SoledadQuerier(soledad=leap_session.soledad_session.soledad)

        yield self.setup_search_engine(
            leap_home,
            soledad_querier)

        self.wrap_mail_store_with_indexing_mail_store(leap_session)

        pixelated_mailboxes = Mailboxes(
            leap_session.account,
            leap_session.mail_store,
            soledad_querier,
            self.search_engine)
        yield pixelated_mailboxes.index_mailboxes()

        self.mail_service = yield self.setup_mail_service(
            leap_session,
            soledad_querier,
            self.search_engine,
            pixelated_mailboxes)

        self.keymanager = leap_session.nicknym
        self.draft_service = self.setup_draft_service(leap_session.mail_store)

        yield self.post_setup(soledad_querier, leap_session)

    def wrap_mail_store_with_indexing_mail_store(self, leap_session):
        leap_session.mail_store = SearchableMailStore(leap_session.mail_store, self.search_engine)

    @defer.inlineCallbacks
    def post_setup(self, soledad_querier, leap_session):
        self.search_engine.index_mails(
            mails=(yield self.mail_service.all_mails()))
        # yield soledad_querier.mark_all_as_not_recent()
        # yield soledad_querier.remove_duplicates()
        InputMail.FROM_EMAIL_ADDRESS = leap_session.account_email()

    @defer.inlineCallbacks
    def setup_search_engine(self, leap_home, soledad_querier):
        key = yield soledad_querier.get_index_masterkey()
        print 'The key len is: %s' % len(key)
        search_engine = SearchEngine(key, agent_home=leap_home)
        MailboxIndexerListener.SEARCH_ENGINE = search_engine
        self.search_engine = search_engine

    @defer.inlineCallbacks
    def setup_mail_service(self, leap_session, soledad_querier, search_engine, pixelated_mailboxes):
        if False:   # FIXME
            yield pixelated_mailboxes.add_welcome_mail_for_fresh_user()
        pixelated_mail_sender = MailSender(
            leap_session.account_email(),
            leap_session.smtp)
        defer.returnValue(MailService(
            pixelated_mailboxes,
            pixelated_mail_sender,
            leap_session.mail_store,
            soledad_querier,
            search_engine))

    def setup_draft_service(self, mail_store):
        return DraftService(mail_store)
