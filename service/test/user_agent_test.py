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
import pixelated.user_agent
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.pixelated_mail import InputMail
from pixelated.adapter.tag import Tag
from pixelated.adapter.tag_service import TagService
from mockito import *
import crochet
import pixelated.reactor_manager as reactor_manager
import test.adapter.test_helper as test_helper
import json
import pixelated.adapter.pixelated_mail
import sys
import os


class UserAgentTest(unittest.TestCase):

    def setUp(self):
        self.app = pixelated.user_agent.app.test_client()
        self.mail_service = mock()

        pixelated.user_agent.DISABLED_FEATURES = []
        pixelated.user_agent.mail_service = self.mail_service
        self.input_mail = None
        pixelated.adapter.pixelated_mail.input_mail_from_dict = lambda x: self.input_mail

    def tearDown(self):
        unstub()

    def test_create_or_send_draft_should_create_draft_if_mail_has_no_ident(self):
        self.input_mail = self.draft()

        self.app.post('/mails', data='{}', content_type="application/json")

        verify(self.mail_service).create_draft(self.input_mail)

    def test_create_or_send_draft_should_send_draft_if_mail_has_ident(self):
        self.input_mail = self.draft()

        self.app.post('/mails', data='{"ident":1}', content_type="application/json")

        verify(self.mail_service).send(1, self.input_mail)

    def test_update_draft(self):
        self.input_mail = self.draft()

        when(self.mail_service).update_draft(1, self.input_mail).thenReturn(self.input_mail)

        self.app.put('/mails', data='{"ident":1}', content_type="application/json")

        verify(self.mail_service).update_draft(1, self.input_mail)

    def draft(self):
        return test_helper.input_mail()

    def test_that_default_config_file_is_home_dot_pixelated(self):
        orig_config = pixelated.user_agent.app.config
        try:
            when(crochet).setup().thenReturn(None)
            when(reactor_manager).start_reactor().thenReturn(None)
            when(pixelated.user_agent).start_user_agent().thenReturn(None)
            pixelated.user_agent.app.config = mock()

            sys.argv = ['/tmp/does_not_exist']
            pixelated.user_agent.setup()

            verify(pixelated.user_agent.app.config).from_pyfile(os.path.join(os.environ['HOME'], '.pixelated'))
        finally:
            pixelated.user_agent.app.config = orig_config

    def test_that_config_file_can_be_specified_on_command_line(self):
        orig_config = pixelated.user_agent.app.config
        try:
            when(crochet).setup().thenReturn(None)
            when(reactor_manager).start_reactor().thenReturn(None)
            when(pixelated.user_agent).start_user_agent().thenReturn(None)
            pixelated.user_agent.app.config = mock()

            sys.argv = ['/tmp/does_not_exist', '--config', '/tmp/some/config/file']
            pixelated.user_agent.setup()

            verify(pixelated.user_agent.app.config).from_pyfile('/tmp/some/config/file')
        finally:
            pixelated.user_agent.app.config = orig_config

    def test_that_tags_returns_all_tags(self):
        when(self.mail_service).all_tags().thenReturn(TagService.SPECIAL_TAGS)

        response = self.app.get('/tags')

        self.assertEqual(200, response.status_code)
        expected = json.dumps([tag.as_dict() for tag in TagService.SPECIAL_TAGS])
        self.assertEqual(expected, response.data)

    def test_that_tags_are_filtered_by_query(self):
        when(self.mail_service).all_tags().thenReturn(TagService.SPECIAL_TAGS)

        response = self.app.get('/tags?q=dr')

        self.assertEqual(200, response.status_code)
        expected = json.dumps([Tag('drafts', True).as_dict()])
        self.assertEqual(expected, response.data)
