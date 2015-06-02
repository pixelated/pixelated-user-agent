from pixelated.config.leap_cert import init_leap_cert


def initialize_leap(leap_provider_cert, leap_provider_cert_fingerprint):
    import pixelated.support.ext_protobuf
    import pixelated.support.ext_sqlcipher
    import pixelated.support.ext_esmtp_sender_factory
    import pixelated.support.ext_fetch
    import pixelated.support.ext_sync
    import pixelated.support.ext_keymanager_fetch_key
    import pixelated.support.ext_requests_urllib3

    init_leap_cert(leap_provider_cert, leap_provider_cert_fingerprint)
