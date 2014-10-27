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
import os
import thread

import pixelated.runserver
from mockito import *
import pixelated.config.reactor_manager as reactor_manager
import pixelated.config.app_factory as app_factory


class RunserverTest(unittest.TestCase):

    def setUp(self):
        when(reactor_manager).start_reactor().thenReturn(None)
        when(app_factory).create_app().thenReturn(None)

    def test_that_config_file_can_be_specified_on_command_line(self):
        orig_config = pixelated.runserver.app.config
        try:
            pixelated.runserver.app.config = mock(dict)
            pixelated.runserver.app.config.__setitem__ = mock()

            sys.argv = ['/tmp/does_not_exist', '--config', '/tmp/some/config/file']
            pixelated.runserver.setup()

            verify(pixelated.runserver.app.config).from_pyfile('/tmp/some/config/file')
        finally:
            pixelated.runserver.app.config = orig_config

    def test_that_organization_switch_reads_the_credentials_from_pipe(self):
        fifo_path = '/tmp/credentials-pipe'
        if os.path.exists(fifo_path):
            os.remove(fifo_path)
        test_fifo = os.mkfifo('/tmp/credentials-pipe')
        thread.start_new_thread(self.spin_up_fifo, (fifo_path,))
        sys.argv = ['tmp/does_not_exist', '--dispatcher']
        pixelated.runserver.credentials_pipe = fifo_path
        pixelated.runserver.setup()

    def spin_up_fifo(self, test_fifo):
        with open(test_fifo, 'w') as fifo:
            fifo.write('test_provider')
            fifo.write('test_user')
            fifo.write('test_password')
