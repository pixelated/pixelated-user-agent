#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
import json

from leap.soledad.client import Soledad
from mockito import mock
import os
from mock import Mock
import shutil
from pixelated.adapter.mail_service import MailService
import pixelated.user_agent
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.pixelated_mailboxes import PixelatedMailBoxes
from pixelated.adapter.soledad_querier import SoledadQuerier

soledad_test_folder = "soledad-test"


class FakeAccount:
    def __init__(self):
        self.mailboxes = ['INBOX', 'DRAFTS', 'SENT', 'TRASH']


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


class SoledadTestBase:

    def __init__(self):
        pass

    def teardown_soledad(self):
        self.soledad.close()
        shutil.rmtree(soledad_test_folder)

    def setup_soledad(self):
        self.app = pixelated.user_agent.app.test_client()
        self.account = FakeAccount()
        self.mail_sender = mock()
        self.mail_address = "test@pixelated.org"
        self.soledad = initialize_soledad(tempdir=soledad_test_folder)

        SoledadQuerier.instance = None
        SoledadQuerier.get_instance(soledad=self.soledad)
        PixelatedMail.from_email_address = self.mail_address
        pixelated_mailboxes = PixelatedMailBoxes(self.account)
        pixelated.user_agent.mail_service = MailService(pixelated_mailboxes, self.mail_sender)

    def get_mails_by_tag(self, tag):
        return json.loads(self.app.get("/mails?q=tag" + tag).data)

    def post_mail(self, data):
        self.app.post('/mails', data=data, content_type="application/json")