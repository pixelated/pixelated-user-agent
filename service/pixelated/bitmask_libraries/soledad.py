import json
import os
import errno
from leap.keymanager import KeyManager
from leap.soledad.client import Soledad
from leap.soledad.common.crypto import WrongMac, UnknownMacMethod, MacMethods
import requests
import sys
import time
from .certs import which_bundle

SOLEDAD_TIMEOUT = 120
SOLEDAD_CERT = '/tmp/ca.crt'


class SoledadDiscoverException(Exception):
    def __init__(self, *args, **kwargs):
        super(SoledadDiscoverException, self).__init__(*args, **kwargs)


class SoledadWrongPassphraseException(Exception):
    def __init__(self, *args, **kwargs):
        super(SoledadWrongPassphraseException, self).__init__(*args, **kwargs)


class LeapKeyManager(object):
    def __init__(self, soledad, leap_session, nicknym_url):
        provider = leap_session.provider
        self.keymanager = KeyManager(leap_session.account_email(), nicknym_url, soledad,
                                     leap_session.session_id, leap_session.leap_home + '/ca.crt', provider.api_uri, leap_session.api_version,
                                     leap_session.uuid, leap_session.leap_config.gpg_binary)


class SoledadSessionFactory(object):
    @classmethod
    def create(cls, provider, srp_session, encryption_passphrase):
        return SoledadSession(provider, encryption_passphrase, srp_session)


class SoledadSession(object):
    def __init__(self, provider, encryption_passphrase, leap_srp_session):
        self.provider = provider
        self.config = provider.config
        self.leap_srp_session = leap_srp_session

        self.soledad = self._init_soledad(encryption_passphrase)

    def _init_soledad(self, encryption_passphrase):
        try:
            server_url = self._discover_soledad_server()

            self._create_database_dir()
            secrets = self._secrets_path()
            local_db = self._local_db_path()

            return Soledad(self.leap_srp_session.uuid, unicode(encryption_passphrase), secrets,
                           local_db, server_url, which_bundle(self.provider), self.leap_srp_session.token)

        except (WrongMac, UnknownMacMethod, MacMethods), e:
            raise SoledadWrongPassphraseException(e)

    def _leap_path(self):
        return "%s/soledad" % self.config.leap_home

    def _secrets_path(self):
        return "%s/%s.secret" % (self._leap_path(), self.leap_srp_session.uuid)

    def _local_db_path(self):
        return "%s/%s.db" % (self._leap_path(), self.leap_srp_session.uuid)

    def _create_database_dir(self):
        try:
            os.makedirs(self._leap_path())
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(self._leap_path()):
                pass
            else:
                raise

    def sync(self):
        if self.soledad.need_sync(self.soledad.server_url):
            self.soledad.sync()

    def _discover_soledad_server(self):
        try:
            json_data = self.provider.fetch_soledad_json()

            hosts = json_data['hosts']
            host = hosts.keys()[0]
            server_url = 'https://%s:%d/user-%s' % \
                         (hosts[host]['hostname'], hosts[host]['port'],
                          self.leap_srp_session.uuid)
            return server_url
        except Exception, e:
            raise SoledadDiscoverException(e)
