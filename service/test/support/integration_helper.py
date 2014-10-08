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
from mockito import mock, unstub
import os
from mock import Mock
import shutil
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.tag_index import TagIndex
from pixelated.adapter.tag_service import TagService
from pixelated.adapter.draft_service import DraftService
import pixelated.user_agent
from pixelated.adapter.pixelated_mail import PixelatedMail, InputMail
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


class MailBuilder:
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

    def with_ident(self, ident):
        self.mail['ident'] = ident
        return self

    def build_json(self):
        return json.dumps(self.mail)

    def build_input_mail(self):
        return InputMail.from_dict(self.mail)


class SoledadTestBase:
    def teardown_soledad(self):
        self.soledad.close()
        shutil.rmtree(soledad_test_folder)

    def setup_soledad(self):
        unstub()  # making sure all mocks from other tests are reset

        self.soledad = initialize_soledad(tempdir=soledad_test_folder)
        self.mail_address = "test@pixelated.org"

        # resetting soledad querier
        SoledadQuerier.reset()
        SoledadQuerier.get_instance(soledad=self.soledad)

        # setup app
        PixelatedMail.from_email_address = self.mail_address
        self.app = pixelated.user_agent.app.test_client()
        self.account = FakeAccount()
        self.pixelated_mailboxes = PixelatedMailBoxes(self.account)
        self.mail_sender = mock()
        self.tag_index = TagIndex(os.path.join(soledad_test_folder, 'tag_index'))
        self.tag_service = TagService(self.tag_index)
        self.draft_service = DraftService(self.pixelated_mailboxes)
        self.mail_service = MailService(self.pixelated_mailboxes, self.mail_sender, self.tag_service)
        self.search_engine = SearchEngine()
        self.search_engine.index_mails(self.mail_service.all_mails())

        pixelated.user_agent.mail_service = self.mail_service
        pixelated.user_agent.draft_service = self.draft_service
        pixelated.user_agent.tag_service = self.tag_service
        pixelated.user_agent.search_engine = self.search_engine

    def get_mails_by_tag(self, tag):
        response = json.loads(self.app.get("/mails?q=tag:" + tag).data)
        return [ResponseMail(m) for m in response['mails']]

    def post_mail(self, data):
        response = json.loads(self.app.post('/mails', data=data, content_type="application/json").data)
        return ResponseMail(response)

    def put_mail(self, data):
        response = json.loads(self.app.put('/mails', data=data, content_type="application/json").data)
        return response['ident']

    def post_tags(self, mail_ident, tags_json):
        return json.loads(
            self.app.post('/mail/' + mail_ident + '/tags', data=tags_json, content_type="application/json").data)

    def delete_mail(self, mail_ident):
        self.app.delete('/mail/' + mail_ident)

    def mark_as_read(self, mail_ident):
        self.app.post('/mail/' + mail_ident + '/read', content_type="application/json")

    def add_mail_to_inbox(self, input_mail):
        mail = self.pixelated_mailboxes.inbox().add(input_mail)
        self.search_engine.index_mail(mail)


class ResponseMail:
    def __init__(self, mail_dict):
        self.mail_dict = mail_dict

    @property
    def subject(self):
        return self.headers['subject']

    @property
    def headers(self):
        return self.mail_dict['header']

    @property
    def ident(self):
        return self.mail_dict['ident']

    @property
    def tags(self):
        return self.mail_dict['tags']

    @property
    def status(self):
        return self.mail_dict['status']
