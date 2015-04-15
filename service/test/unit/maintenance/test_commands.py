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

from pixelated.maintenance import delete_all_mails
from pixelated.bitmask_libraries.session import LeapSession
from leap.soledad.client import Soledad
from leap.soledad.common.document import SoledadDocument
from mock import MagicMock


class TestCommands(unittest.TestCase):

        def setUp(self):
            self.leap_session = MagicMock(spec=LeapSession)
            self.soledad = MagicMock(spec=Soledad)
            self.args = (self.leap_session, self.soledad)

        def test_delete_all_mails_supports_empty_doclist(self):
            self.soledad.get_all_docs.return_value = (1, [])

            delete_all_mails(self.args)

            self.assertFalse(self.soledad.delete_doc.called)

        def test_delete_all_mails(self):
            doc = MagicMock(spec=SoledadDocument)
            doc.content = {'type': 'head'}
            self.soledad.get_all_docs.return_value = (1, [doc])

            delete_all_mails(self.args)

            self.soledad.delete_doc.assert_called_once_with(doc)

        def test_only_mail_documents_are_deleted(self):
            docs = self._create_docs_of_type(['head', 'cnt', 'flags', 'mbx', 'foo', None])
            self.soledad.get_all_docs.return_value = (1, docs)

            delete_all_mails(self.args)

            for doc in docs:
                if doc.content['type'] in ['head', 'cnt', 'flags']:
                    self.soledad.delete_doc.assert_any_call(doc)
            self.assertEqual(3, len(self.soledad.delete_doc.mock_calls))

        def _create_docs_of_type(self, type_list):
            return [self._create_doc_type(t) for t in type_list]

        def _create_doc_type(self, doc_type):
            doc = MagicMock(spec=SoledadDocument)
            doc.content = {'type': doc_type}
            return doc
