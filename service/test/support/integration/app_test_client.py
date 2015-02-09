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
import multiprocessing
import shutil
import time

from leap.mail.imap.account import SoledadBackedAccount
from leap.soledad.client import Soledad
from mock import MagicMock, Mock
import os
from pixelated.adapter.services.draft_service import DraftService
from pixelated.adapter.services.mail_service import MailService
from pixelated.adapter.services.mailboxes import Mailboxes
from pixelated.adapter.soledad.soledad_querier import SoledadQuerier
from pixelated.adapter.services.tag_service import TagService
from pixelated.config import App
from pixelated.resources.root_resource import RootResource
from pixelated.adapter.model.mail import PixelatedMail
from pixelated.adapter.search import SearchEngine
from test.support.integration import MailBuilder
from test.support.test_helper import request_mock
from twisted.internet import reactor
from twisted.internet.defer import succeed
from twisted.web.resource import getChildForRequest
from twisted.web.server import Site
import uuid


class AppTestClient:
    INDEX_KEY = '\xde3?\x87\xff\xd9\xd3\x14\xf0\xa7>\x1f%C{\x16.\\\xae\x8c\x13\xa7\xfb\x04\xd4]+\x8d_\xed\xd1\x8d\x0bI' \
                '\x8a\x0e\xa4tm\xab\xbf\xb4\xa5\x99\x00d\xd5w\x9f\x18\xbc\x1d\xd4_W\xd2\xb6\xe8H\x83\x1b\xd8\x9d\xad'

    def __init__(self, soledad_test_folder='/tmp/soledad-test/test'):

        soledad_test_folder = os.path.join(soledad_test_folder, str(uuid.uuid4()))
        self.soledad = initialize_soledad(tempdir=soledad_test_folder)
        self.cleanup = lambda: shutil.rmtree(soledad_test_folder)

        self.mail_address = "test@pixelated.org"

        # setup app
        PixelatedMail.from_email_address = self.mail_address

        SearchEngine.DEFAULT_INDEX_HOME = soledad_test_folder

        self.app = App()

        self.soledad_querier = SoledadQuerier(self.soledad)
        self.soledad_querier.get_index_masterkey = lambda: self.INDEX_KEY

        self.account = SoledadBackedAccount('test', self.soledad, MagicMock())
        self.search_engine = SearchEngine(self.soledad_querier, agent_home=soledad_test_folder)
        self.mailboxes = Mailboxes(self.account, self.soledad_querier, self.search_engine)
        self.mail_sender = Mock()
        self.tag_service = TagService()
        self.draft_service = DraftService(self.mailboxes)
        self.mail_service = MailService(self.mailboxes, self.mail_sender, self.tag_service,
                                        self.soledad_querier, self.search_engine)
        self.search_engine.index_mails(self.mail_service.all_mails())

        self.app.resource = RootResource()

        # sending a mail is always successful
        self.mail_sender.sendmail.side_effect = lambda mail: succeed(mail)

        self.app.resource.initialize(self.soledad_querier, self.search_engine, self.mail_service, self.draft_service)

    def _render(self, request, as_json=True):
        def get_str(_str):
            return json.loads(_str) if as_json else _str

        def get_request_written_data(_=None):
            written_data = request.getWrittenData()
            if written_data:
                return get_str(written_data)

        resource = getChildForRequest(self.app.resource, request)
        result = resource.render(request)

        if isinstance(result, basestring):
            return get_str(result), request

        # result is NOT_DONE_YET
        d = succeed(request) if request.finished else request.notifyFinish()
        d.addCallback(get_request_written_data)
        return d, request

    def run_on_a_thread(self, logfile='/tmp/app_test_client.log', port=4567, host='0.0.0.0'):
        def _start():
            reactor.listenTCP(port, Site(self.app.resource), interface=host)
            reactor.run()
        process = multiprocessing.Process(target=_start)
        process.start()
        time.sleep(1)
        return lambda: process.terminate()

    def get(self, path, get_args='', as_json=True):
        request = request_mock(path)
        request.args = get_args
        return self._render(request, as_json)

    def post(self, path, body=''):
        request = request_mock(path=path, method="POST", body=body, headers={'Content-Type': ['application/json']})
        return self._render(request)

    def put(self, path, body):
        request = request_mock(path=path, method="PUT", body=body, headers={'Content-Type': ['application/json']})
        return self._render(request)

    def delete(self, path, body=""):
        request = request_mock(path=path, body=body, headers={'Content-Type': ['application/json']}, method="DELETE")
        return self._render(request)

    def add_document_to_soledad(self, _dict):
        self.soledad_querier.soledad.create_doc(_dict)

    def add_mail_to_inbox(self, input_mail):
        mail = self.mailboxes.inbox().add(input_mail)
        mail.update_tags(input_mail.tags)
        self.search_engine.index_mail(mail)

    def add_multiple_to_mailbox(self, num, mailbox='', flags=[], tags=[], to='recipient@to.com', cc='recipient@cc.com', bcc='recipient@bcc.com'):
        mails = []
        for _ in range(num):
            input_mail = MailBuilder().with_status(flags).with_tags(tags).with_to(to).with_cc(cc).with_bcc(bcc).build_input_mail()
            mail = self.mailboxes._create_or_get(mailbox).add(input_mail)
            mails.append(mail)
            mail.update_tags(input_mail.tags)
            self.search_engine.index_mail(mail)
        return mails


def initialize_soledad(tempdir):
    if os.path.isdir(tempdir):
        shutil.rmtree(tempdir)

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
        cert_file,
        defer_encryption=False)
    return _soledad
