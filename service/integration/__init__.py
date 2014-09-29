import json

from leap.soledad.client import Soledad
import os
from mock import Mock


def initialize_soledad(tempdir):
    uuid = "foobar-uuid"
    passphrase = u"verysecretpassphrase"
    secret_path = os.path.join(tempdir, "secret.gpg")
    local_db_path = os.path.join(tempdir, "soledad.u1db")
    server_url = "http://provider"
    cert_file = ""

    class MockSharedDB(object):

        get_doc = Mock(return_value=None)
        put_doc = Mock()
        lock = Mock(return_value=('atoken', 300))
        unlock = Mock(return_value=True)

        def __call__(self):
            return self

    Soledad._shared_db = MockSharedDB()

    _soledad = Soledad(
        uuid,
        passphrase,
        secret_path,
        local_db_path,
        server_url,
        cert_file)

    from leap.mail.imap.fields import fields
    for name, expression in fields.INDEXES.items():
        _soledad.create_index(name, *expression)

    return _soledad


class JSONMailBuilder:
    def __init__(self):
        self.mail = {
            'header': {
                'to': ['recipient@to.com'],
                'cc': ['recipient@cc.com'],
                'bcc': ['recipient@bcc.com'],
                'subject': 'Hi! This the subject'
            },
            'body': "Hello,\nThis is the body of this message\n\nRegards,\n\n--\nPixelated.\n"
        }

    def with_body(self, body):
        self.mail['body'] = body
        return self

    def with_subject(self, subject):
        self.mail['header']['subject'] = subject
        return self

    def build(self):
        return json.dumps(self.mail)