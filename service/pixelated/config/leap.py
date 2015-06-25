from __future__ import absolute_import
import random
from pixelated.config import credentials
from leap.common.events import server as events_server
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.bitmask_libraries.session import LeapSessionFactory


def initialize_leap(leap_provider_cert,
                    leap_provider_cert_fingerprint,
                    credentials_file,
                    organization_mode,
                    leap_home):
    init_monkeypatches()
    events_server.ensure_server(random.randrange(8000, 11999))
    provider, username, password = credentials.read(organization_mode, credentials_file)
    LeapCertificate.set_cert_and_fingerprint(leap_provider_cert, leap_provider_cert_fingerprint)

    config = LeapConfig(leap_home=leap_home, start_background_jobs=True)
    provider = LeapProvider(provider, config)
    LeapCertificate(provider).setup_ca_bundle()
    leap_session = LeapSessionFactory(provider).create(username, password)

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
