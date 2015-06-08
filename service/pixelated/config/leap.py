from __future__ import absolute_import
import random
from pixelated.config import credentials
from leap.common.events import server as events_server
from pixelated.bitmask_libraries import certs
from pixelated.bitmask_libraries.session import open_leap_session


def initialize_leap(leap_provider_cert,
                    leap_provider_cert_fingerprint,
                    credentials_file,
                    organization_mode,
                    leap_home):
    init_monkeypatches()
    provider, user, password = credentials.read(organization_mode, credentials_file)
    certs.init_leap_cert(leap_provider_cert, leap_provider_cert_fingerprint)
    events_server.ensure_server(random.randrange(8000, 11999))
    leap_session = create_leap_session(provider, user, password, leap_home)
    leap_session.start_background_jobs()
    return leap_session


def create_leap_session(provider, username, password, leap_home):
    leap_session = open_leap_session(username,
                                     password,
                                     provider,
                                     leap_home)
    leap_session.soledad_session.soledad.sync(defer_decryption=False)
    leap_session.nicknym.generate_openpgp_key()
    return leap_session


def init_monkeypatches():
    import pixelated.extensions.protobuf_socket
    import pixelated.extensions.sqlcipher_wal
    import pixelated.extensions.esmtp_sender_factory
    import pixelated.extensions.incoming_decrypt_header
    import pixelated.extensions.soledad_sync_exception
    import pixelated.extensions.keymanager_fetch_key
    import pixelated.extensions.requests_urllib3
    import pixelated.extensions.shared_db
