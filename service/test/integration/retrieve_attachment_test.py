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

from test.support.integration_helper import SoledadTestBase


class RetrieveAttachmentTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    def tearDown(self):
        SoledadTestBase.tearDown(self)

    def test_attachment_content_is_retrieved(self):
        ident = 'F4E99C1CEC4D300A4223A96CCABBE0304BDBC31C550A5A03E207A5E4C3C71A22'
        attachment_dict = {'content-disposition': 'attachment',
                           'content-transfer-encoding': '',
                           'type': 'cnt',
                           'raw': 'cGVxdWVubyBhbmV4byA6RAo=',
                           'phash': ident,
                           'content-type': 'text/plain; charset=US-ASCII; name="attachment_pequeno.txt"'}

        self.add_document_to_soledad(attachment_dict)

        attachment = self.get_attachment(ident, 'base64')

        self.assertEquals('pequeno anexo :D\n', attachment)
