from pixelated.config.config import Config
from pixelated.config import credentials
from leap.common.events import server as events_server
import pixelated.bitmask_libraries.certs as certs
from pixelated.bitmask_libraries.session import open_leap_session


def initialize_leap(leap_provider_cert,
                    leap_provider_cert_fingerprint,
                    credentials_file,
                    organization_mode,
                    leap_home):
    init_monkeypatches()
    provider, user, password = credentials.read(organization_mode, credentials_file)
    init_leap_cert(leap_provider_cert, leap_provider_cert_fingerprint)
    events_server.ensure_server(port=8090)
    leap_session = create_leap_session(provider, user, password, leap_home)
    return leap_session


def create_leap_session(provider, username, password, leap_home):
    leap_session = open_leap_session(username,
                                     password,
                                     provider,
                                     leap_home)
    leap_session.soledad_session.soledad.sync(defer_decryption=False)
    leap_session.nicknym.generate_openpgp_key()
    return leap_session


def init_leap_cert(leap_provider_cert, leap_provider_cert_fingerprint):
    if leap_provider_cert_fingerprint is None:
        certs.LEAP_CERT = leap_provider_cert or True
        certs.LEAP_FINGERPRINT = None
    else:
        certs.LEAP_FINGERPRINT = leap_provider_cert_fingerprint
        certs.LEAP_CERT = False


def init_monkeypatches():
    import pixelated.support.ext_protobuf
    import pixelated.support.ext_sqlcipher
    import pixelated.support.ext_esmtp_sender_factory
    import pixelated.support.ext_fetch
    import pixelated.support.ext_sync
    import pixelated.support.ext_keymanager_fetch_key
    import pixelated.support.ext_requests_urllib3
    import pixelated.support.ext_shared_db
