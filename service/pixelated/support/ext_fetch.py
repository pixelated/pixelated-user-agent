import leap.mail.imap.fetch as fetch


def mark_as_encrypted_inline(f):

    def w(*args, **kwargs):
        msg, valid_sign = f(*args)
        is_encrypted = fetch.PGP_BEGIN in args[1].as_string() and fetch.PGP_END in args[1].as_string()
        decrypted_successfully = not fetch.PGP_BEGIN in msg.as_string() and not fetch.PGP_END in msg.as_string()

        if not is_encrypted:
            encrypted = 'false'
        else:
            if decrypted_successfully:
                encrypted = 'true'
            else:
                encrypted = 'fail'

        msg.add_header('X-Pixelated-encryption-status', encrypted)
        return msg, valid_sign

    return w


def mark_as_encrypted_multipart(f):

    def w(*args, **kwargs):
        msg, valid_sign = f(*args)
        msg.add_header('X-Pixelated-encryption-status', 'true')
        return msg, valid_sign
    return w


fetch.LeapIncomingMail._maybe_decrypt_inline_encrypted_msg = mark_as_encrypted_inline(fetch.LeapIncomingMail._maybe_decrypt_inline_encrypted_msg)
fetch.LeapIncomingMail._decrypt_multipart_encrypted_msg = mark_as_encrypted_multipart(fetch.LeapIncomingMail._decrypt_multipart_encrypted_msg)
