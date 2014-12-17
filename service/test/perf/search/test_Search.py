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
import unittest
import json

from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data
from test.support.integration import AppTestClient


class Search(FunkLoadTestCase):

    def setUpBench(self):
        client = AppTestClient()

        # setup data
        client.add_multiple_to_mailbox(10, 'INBOX', to='to@inbox.com', cc='cc@inbox.com', bcc='bcc@inbox.com', tags=['inbox'])
        client.add_multiple_to_mailbox(10, 'TRASH', to='to@trash.com', cc='cc@trash.com', bcc='bcc@trash.com', tags=['trash'])
        client.add_multiple_to_mailbox(10, 'DRAFTS', to='to@drafts.com', cc='cc@drafts.com', bcc='bcc@drafts.com', tags=['drafts'])

        self.call_to_terminate = client.run_on_a_thread(logfile='results/app.log')

    def tearDownBench(self):
        self.call_to_terminate()

    def setUp(self):
        """Setting up test."""
        self.server_url = self.conf_get('main', 'url')
        self.mails_by_tag_url = self.server_url + '/mails?q=%%22tag:%s%%22&w=25&p=0'

    def idents_by_tag(self, tag):
        return list(mail['ident'] for mail in json.loads(self.get(self.mails_by_tag_url % tag, description='Query mails by tag').body)['mails'])

    def test_search(self):
        """ Query contacts and tags. Write a new tag, updating index. Query again. """
        contacts_url = self.server_url + '/contacts?q=rec'
        mail_tags_url = self.server_url + '/mail/%s/tags'
        all_tags_url = self.server_url + '/tags'
        tags = ['inbox', 'trash', 'drafts']
        nb_time = self.conf_getInt('main', 'nb_time')

        for i in range(nb_time):
            self.get(contacts_url, description='Query for contacts')
            idents = self.idents_by_tag(tags[i % 3])
            tag_data = Data('application/json', '{"newtags":["newtag%s"]}' % i)
            self.post(mail_tags_url % idents[i % 3], tag_data, description='Change tags on a mail')
            self.idents_by_tag(tags[i % 3])
            self.get(all_tags_url, description='Query for all tags listing')

if __name__ in ('main', '__main__'):
    unittest.main()
