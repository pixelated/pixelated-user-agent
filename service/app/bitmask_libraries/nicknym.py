from leap.keymanager import KeyManager
from .certs import which_bundle

SOLEDAD_CERT = '/tmp/ca.crt'


class NickNym(object):

    def __init__(self, provider, config, soledad_session, srp_session):
        nicknym_url = _discover_nicknym_server(provider)
        self.keymanager = KeyManager('%s@%s' % (srp_session.user_name, provider.domain), nicknym_url, soledad_session.soledad,
                                     srp_session.session_id, which_bundle(provider), provider.api_uri,
                                     provider.api_version,
                                     srp_session.uuid, config.gpg_binary)


def _discover_nicknym_server(provider):
        return 'https://nicknym.%s:6425/' % provider.domain
