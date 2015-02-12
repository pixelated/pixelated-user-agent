import leap.mail.imap.fetch as fetch


def mark_as_encrypted(f):

    def w(*args, **kwargs):
        msg, was_decrypted = f(*args)
        msg.add_header('X-Pixelated-encryption-status', 'true' if was_decrypted else 'false')
        return msg, was_decrypted
    return w


fetch.LeapIncomingMail._maybe_decrypt_inline_encrypted_msg = mark_as_encrypted(fetch.LeapIncomingMail._maybe_decrypt_inline_encrypted_msg)
fetch.LeapIncomingMail._decrypt_multipart_encrypted_msg = mark_as_encrypted(fetch.LeapIncomingMail._decrypt_multipart_encrypted_msg)
