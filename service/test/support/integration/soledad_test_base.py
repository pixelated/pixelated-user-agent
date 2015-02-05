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
from twisted.trial import unittest
from pixelated.resources import *
from test.support.integration.app_test_client import AppTestClient
from test.support.integration.model import ResponseMail


class SoledadTestBase(unittest.TestCase):
    # these are so long because our CI is so slow at the moment.
    DEFERRED_TIMEOUT = 120
    DEFERRED_TIMEOUT_LONG = 300

    def setUp(self):
        self.client = AppTestClient()

    def tearDown(self):
        self.client.cleanup()

    def get_mails_by_tag(self, tag, page=1, window=100):
        tags = 'tag:%s' % tag
        return self.search(tags, page, window)

    def search(self, query, page=1, window=100):
        res, req = self.client.get("/mails", {
            'q': [query],
            'w': [str(window)],
            'p': [str(page)]
        })
        return [ResponseMail(m) for m in res['mails']]

    def get_attachment(self, ident, encoding):
        res, req = self.client.get("/attachment/%s" % ident, {'encoding': [encoding]}, as_json=False)
        return res

    def put_mail(self, data):
        res, req = self.client.put('/mails', data)
        return res, req

    def post_tags(self, mail_ident, tags_json):
        res, req = self.client.post("/mail/%s/tags" % mail_ident, tags_json)
        return res

    def get_tags(self, **kwargs):
        res, req = self.client.get('/tags', kwargs)
        return res

    def get_mail(self, mail_ident):
        res, req = self.client.get('/mail/%s' % mail_ident)
        return res

    def delete_mail(self, mail_ident):
        res, req = self.client.delete("/mail/%s" % mail_ident)
        return req

    def delete_mails(self, idents):
        res, req = self.client.post("/mails/delete", json.dumps({'idents': idents}))
        return req

    def mark_many_as_unread(self, idents):
        res, req = self.client.post('/mails/unread', json.dumps({'idents': idents}))
        return req

    def mark_many_as_read(self, idents):
        res, req = self.client.post('/mails/read', json.dumps({'idents': idents}))
        return req

    def get_contacts(self, query):
        res, req = self.client.get('/contacts', get_args={'q': query})
        return res
