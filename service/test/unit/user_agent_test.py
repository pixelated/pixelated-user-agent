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
import sys

import pixelated.user_agent
from mockito import *
import crochet
import pixelated.reactor_manager as reactor_manager
import test.support.test_helper as test_helper
import pixelated.adapter.pixelated_mail
import os


class UserAgentTest(unittest.TestCase):

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
