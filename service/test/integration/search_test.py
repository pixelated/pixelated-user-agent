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

from test.support.integration_helper import MailBuilder, SoledadTestBase


class SearchTest(unittest.TestCase, SoledadTestBase):

    def setUp(self):
        self.setup_soledad()

    def tearDown(self):
        self.teardown_soledad()

    def test_that_tags_returns_all_tags(self):
        input_mail = MailBuilder().with_tags('important').build_input_mail()
        self.add_mail_to_inbox(input_mail)

        all_tags = self.get_tags()

        all_tag_names = [t['name'] for t in all_tags]
        self.assertTrue('inbox' in all_tag_names)
        self.assertTrue('sent' in all_tag_names)
        self.assertTrue('trash' in all_tag_names)
        self.assertTrue('drafts' in all_tag_names)
        self.assertTrue('important' in all_tag_names)

    def test_that_tags_are_filtered_by_query(self):
        input_mail = MailBuilder().with_tags('mytag').build_input_mail()
        self.add_mail_to_inbox(input_mail)

        all_tags = self.get_tags('?q=my&skipDefaultTags=true')

        all_tag_names = [t['name'] for t in all_tags]
        self.assertEqual(1, len(all_tag_names))
        self.assertTrue('mytag' in all_tag_names)

    def test_that_default_tags_are_ignorable(self):
        input_mail = MailBuilder().with_tags('sometag').build_input_mail()
        self.add_mail_to_inbox(input_mail)

        all_tags = self.get_tags('?skipDefaultTags=true')

        all_tag_names = [t['name'] for t in all_tags]
        self.assertEqual(1, len(all_tag_names))
        self.assertTrue('sometag' in all_tag_names)
