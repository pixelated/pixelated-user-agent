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
import errno
import traceback
import sys

import os
from leap.mail.incoming.service import IncomingMail
from twisted.internet import reactor
from .nicknym import NickNym
from leap.auth import SRPAuth
from .soledad import SoledadSessionFactory
from .smtp import LeapSmtp
from leap.mail.imap.account import IMAPAccount
from twisted.internet import defer

SESSIONS = {}


class LeapSession(object):
    """
    A LEAP session.


    Properties:

    - ``smtp`` the smtp gateway instance (LeapSmtp).

    - ``config`` the configuration for this session (LeapClientConfig).

    - ``provider`` the responsible for interacting with provider.json (LeapProvider).

    - ``user_auth`` the secure remote password session data after authenticating with LEAP. See http://en.wikipedia.org/wiki/Secure_Remote_Password_protocol (SRPSession)

    - ``soledad_session`` the soledad session. See https://leap.se/soledad (LeapSecureRemotePassword)

    - ``nicknym`` the nicknym instance. See https://leap.se/nicknym (NickNym)

    - ``incoming_mail_fetcher`` Background job for fetching incoming mails from LEAP server (LeapIncomingMail)
    """

    def __init__(self, provider, user_auth, soledad_session, nicknym, soledad_account, incoming_mail_fetcher, smtp):
        self.smtp = smtp
        self.config = provider.config
        self.provider = provider
        self.user_auth = user_auth
        self.soledad_session = soledad_session
        self.nicknym = nicknym
        self.account = soledad_account
        self.incoming_mail_fetcher = incoming_mail_fetcher

        d = self.sync()
        d.addCallback(lambda _: self.nicknym.generate_openpgp_key())

        if self.config.start_background_jobs:
            d.addCallback(lambda _: self.start_background_jobs())

    def account_email(self):
        name = self.user_auth.username
        return self.provider.address_for(name)

    def close(self):
        self.stop_background_jobs()

    @defer.inlineCallbacks
    def start_background_jobs(self):
        self.incoming_mail_fetcher = yield self.incoming_mail_fetcher
        reactor.callFromThread(self.incoming_mail_fetcher.startService)

    def stop_background_jobs(self):
        reactor.callFromThread(self.incoming_mail_fetcher.stopService)

    def sync(self):
        try:
            return self.soledad_session.sync()
        except:
            traceback.print_exc(file=sys.stderr)
            raise


class LeapSessionFactory(object):
    def __init__(self, provider):
        self._provider = provider
        self._config = provider.config

    def create(self, username, password):
        key = self._session_key(username)
        session = self._lookup_session(key)
        if not session:
            session = self._create_new_session(username, password)
            self._remember_session(key, session)

        return session

    def _create_new_session(self, username, password):
        self._create_dir(self._provider.config.leap_home)
        self._provider.download_certificate()

        srp_auth = SRPAuth(self._provider.api_uri, self._provider.local_ca_crt)
        auth = srp_auth.authenticate(username, password)
        account_email = self._provider.address_for(username)

        soledad = SoledadSessionFactory.create(self._provider, auth.token, auth.uuid, password)

        nicknym = self._create_nicknym(account_email, auth.token, auth.uuid, soledad)
        account = self._create_account(account_email, soledad)
        deferred_incoming_mail_fetcher = self._create_incoming_mail_fetcher(nicknym, soledad, account, account_email)

        smtp = LeapSmtp(self._provider, auth, nicknym.keymanager)

        return LeapSession(self._provider, auth, soledad, nicknym, account, deferred_incoming_mail_fetcher, smtp)

    def _lookup_session(self, key):
        global SESSIONS
        if key in SESSIONS:
            return SESSIONS[key]
        else:
            return None

    def _remember_session(self, key, session):
        global SESSIONS
        SESSIONS[key] = session

    def _session_key(self, username):
        return hash((self._provider, username))

    def _create_dir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _create_nicknym(self, email_address, token, uuid, soledad_session):
        return NickNym(self._provider, self._config, soledad_session, email_address, token, uuid)

    def _create_account(self, user_mail, soledad_session):
        account = IMAPAccount(user_mail, soledad_session.soledad)
        return account
        # memstore = MemoryStore(permanent_store=SoledadStore(soledad_session.soledad))
        # return SoledadBackedAccount(uuid, soledad_session.soledad, memstore)

    @defer.inlineCallbacks
    def _create_incoming_mail_fetcher(self, nicknym, soledad_session, account, user_mail):
        # FIXME Replace inbox collection by our own mailbox indexer
        inbox = yield account.getMailbox('INBOX')
        defer.returnValue(IncomingMail(nicknym.keymanager,
                          soledad_session.soledad,
                          inbox,
                          user_mail))
