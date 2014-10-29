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
from pixelated.adapter.soledad_querier import SoledadQuerier
from mockito import mock, when, any
import json
import os
import base64
import quopri


class SoledadQuerierTest(unittest.TestCase):

    def test_extract_parts(self):
        soledad = mock()
        bdoc = mock()
        bdoc.content = {'raw': 'esse papo seu ta qualquer coisa'}
        when(soledad).get_from_index('by-type-and-payloadhash', 'cnt', any(unicode)).thenReturn([bdoc])
        multipart_attachment_file = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'multipart_attachment.json')
        with open(multipart_attachment_file) as f:
            hdoc = json.loads(f.read())
        querier = SoledadQuerier(soledad)

        parts = querier._extract_parts(hdoc)

        self.assertIn('alternatives', parts.keys())
        self.assertIn('attachments', parts.keys())
        self.assertEquals(2, len(parts['alternatives']))
        self.assertEquals(1, len(parts['attachments']))

        self.check_alternatives(parts)
        self.check_attachments(parts)

    def check_alternatives(self, parts):
        for alternative in parts['alternatives']:
            self.assertIn('headers', alternative)
            self.assertIn('content', alternative)

    def check_attachments(self, parts):
        for attachment in parts['attachments']:
            self.assertIn('headers', attachment)
            self.assertIn('ident', attachment)
            self.assertIn('name', attachment)

    def test_extract_part_without_headers(self):
        soledad = mock()
        bdoc = mock()
        bdoc.content = {'raw': 'esse papo seu ta qualquer coisa'}
        when(soledad).get_from_index('by-type-and-payloadhash', 'cnt', any(unicode)).thenReturn([bdoc])
        hdoc = {'multi': True, 'part_map': {'1': {'multi': False, 'phash': u'0400BEBACAFE'}}}
        querier = SoledadQuerier(soledad)

        parts = querier._extract_parts(hdoc)

        self.assertEquals(bdoc.content['raw'], parts['alternatives'][0]['content'])

    def test_attachment_base64(self):
        soledad = mock()
        bdoc = mock()
        bdoc.content = {'raw': base64.encodestring('esse papo seu ta qualquer coisa'), 'content-type': 'text/plain'}
        when(soledad).get_from_index('by-type-and-payloadhash', 'cnt', any(unicode)).thenReturn([bdoc])
        querier = SoledadQuerier(soledad)

        attachment = querier.attachment(u'0400BEBACAFE', 'base64')

        self.assertEquals('esse papo seu ta qualquer coisa', attachment['content'])

    def test_attachment_quoted_printable(self):
        soledad = mock()
        bdoc = mock()
        bdoc.content = {'raw': quopri.encodestring('esse papo seu ta qualquer coisa'), 'content-type': 'text/plain'}
        when(soledad).get_from_index('by-type-and-payloadhash', 'cnt', any(unicode)).thenReturn([bdoc])
        querier = SoledadQuerier(soledad)

        attachment = querier.attachment(u'0400BEBACAFE', 'quoted-printable')

        self.assertEquals('esse papo seu ta qualquer coisa', attachment['content'])
