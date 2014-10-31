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
import shutil
from klein.resource import KleinResource

from leap.soledad.client import Soledad
from mockito import mock
import os
from mock import Mock, MagicMock
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.status import Status
from pixelated.adapter.tag_service import TagService
from pixelated.adapter.draft_service import DraftService
from pixelated.adapter.mail import PixelatedMail, InputMail
import pixelated.runserver
from pixelated.adapter.mailboxes import Mailboxes
from pixelated.adapter.soledad_querier import SoledadQuerier
from pixelated.controllers import *
import pixelated.config.app_factory as app_factory
from leap.mail.imap.account import SoledadBackedAccount
from klein.test_resource import requestMock, _render


soledad_test_folder = "soledad-test"


def initialize_soledad(tempdir):
    if os.path.isdir(soledad_test_folder):
        shutil.rmtree(soledad_test_folder)

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
        close = Mock()

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
    #
    # from leap.mail.imap.fields import fields
    #
    # for name, expression in fields.INDEXES.items():
    # _soledad.create_index(name, *expression)
    #
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
            'body': "Hello,\nThis is the body of this message\n\nRegards,\n\n--\nPixelated.\n",
            'status': []
        }

    def with_body(self, body):
        self.mail['body'] = body
        return self

    def with_tags(self, tags):
        self.mail['tags'] = tags
        return self

    def with_subject(self, subject):
        self.mail['header']['subject'] = subject
        return self

    def with_status(self, flags):
        for status in Status.from_flags(flags):
            self.mail['status'].append(status)
        return self

    def with_date(self, date_string):
        self.mail['header']['date'] = date_string
        return self

    def with_ident(self, ident):
        self.mail['ident'] = ident
        return self

    def build_json(self):
        return json.dumps(self.mail)

    def build_input_mail(self):
        return InputMail.from_dict(self.mail)


class SoledadTestBase:
    def __init__(self):
        pass

    def teardown_soledad(self):
        pass

    def setup_soledad(self):
        self.soledad = initialize_soledad(tempdir=soledad_test_folder)
        self.mail_address = "test@pixelated.org"

        # setup app
        PixelatedMail.from_email_address = self.mail_address

        SearchEngine.INDEX_FOLDER = soledad_test_folder + '/search_index'

        self.app = pixelated.runserver.app

        self.soledad_querier = SoledadQuerier(self.soledad)

        self.account = SoledadBackedAccount('test', self.soledad, MagicMock())
        self.mailboxes = Mailboxes(self.account, self.soledad_querier)
        self.mail_sender = mock()
        self.tag_service = TagService()
        self.draft_service = DraftService(self.mailboxes)
        self.mail_service = MailService(self.mailboxes, self.mail_sender, self.tag_service,
                                        self.soledad_querier)
        self.search_engine = SearchEngine()
        self.search_engine.index_mails(self.mail_service.all_mails())

        features_controller = FeaturesController()
        features_controller.DISABLED_FEATURES.append('autoReload')
        home_controller = HomeController()
        mails_controller = MailsController(mail_service=self.mail_service,
                                           draft_service=self.draft_service,
                                           search_engine=self.search_engine)
        tags_controller = TagsController(search_engine=self.search_engine)
        sync_info_controller = SyncInfoController()
        attachments_controller = AttachmentsController(self.soledad_querier)

        app_factory._setup_routes(self.app, home_controller, mails_controller, tags_controller,
                                  features_controller, sync_info_controller, attachments_controller)
        self.resource = KleinResource(self.app)

    def get_mails_by_tag(self, tag, page=1, window=100):
        request = requestMock(path="/mails")
        request.args = {
            'q': ['tag:%s' % tag],
            'w': [str(window)],
            'p': [str(page)]
        }
        _render(self.resource, request)
        response = json.loads(request.getWrittenData())
        return [ResponseMail(m) for m in response['mails']]

    def post_mail(self, data):
        request = requestMock(path='/mails', method="POST", body=data, headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        response = json.loads(request.getWrittenData())
        return ResponseMail(response)

    def put_mail(self, data):
        request = requestMock('/mails', method="PUT", body=data, headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        response = json.loads(request.getWrittenData())
        return response['ident']

    def post_tags(self, mail_ident, tags_json):
        request = requestMock('/mail/' + mail_ident + '/tags', method="POST", body=tags_json,
                              headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        return json.loads(request.getWrittenData())

    def get_tags(self, **kwargs):
        request = requestMock('/tags')
        request.args = kwargs
        _render(self.resource, request)
        return json.loads(request.getWrittenData())

    def delete_mail(self, mail_ident):
        request = requestMock(path='/mail/' + mail_ident, method="DELETE")
        _render(self.resource, request)
        return request

    def mark_as_read(self, mail_ident):
        request = requestMock('/mail/' + mail_ident + '/read', method="POST", headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        return request

    def mark_as_unread(self, mail_ident):
        request = requestMock('/mail/' + mail_ident + '/unread', method="POST", headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        return request

    def mark_many_as_unread(self, idents):
        request = requestMock('/mails/unread', method="POST", body=json.dumps({'idents': idents}), headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        return request

    def mark_many_as_read(self, idents):
        request = requestMock('/mails/read', method="POST", body=json.dumps({'idents': idents}), headers={'Content-Type': ['application/json']})
        _render(self.resource, request)
        return request

    def add_mail_to_inbox(self, input_mail):
        mail = self.mailboxes.inbox().add(input_mail)
        mail.update_tags(input_mail.tags)
        self.search_engine.index_mail(mail)

    def add_multiple_to_mailbox(self, num, mailbox='', flags=[], tags=[]):
        mails = []
        for _ in range(num):
            input_mail = MailBuilder().with_status(flags).with_tags(tags).build_input_mail()
            mail = self.mailboxes._create_or_get(mailbox).add(input_mail)
            mails.append(mail)
            mail.update_tags(input_mail.tags)
            self.search_engine.index_mail(mail)
        return mails


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
