from pixelated.config.config import Config
from pixelated.config.config_ua import config_user_agent
from pixelated.config.dispatcher import config_dispatcher
import pixelated.bitmask_libraries.certs as certs


def initialize_leap(leap_provider_cert,
                    leap_provider_cert_fingerprint,
                    config_file,
                    dispatcher,
                    dispatcher_stdin):

    init_monkeypatches()

    provider, user, password = gather_credentials(dispatcher,
                                                  dispatcher_stdin,
                                                  config_file)

    config = Config()
    config.provider = provider
    config.username = user
    config.password = password

    init_leap_cert(leap_provider_cert, leap_provider_cert_fingerprint)

    return config


def gather_credentials(dispatcher, dispatcher_stdin, config_file):
    if dispatcher or dispatcher_stdin:
        return config_dispatcher(dispatcher)
    else:
        return config_user_agent(config_file)


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
