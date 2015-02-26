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

import logging
import socket
import sys
import os
from twisted.python import log
from twisted.python import util


LOG_FILE = '/tmp/pixelated.log'


def init_logging(args):
    pixelated_log_format = '[%(asctime)s] ' + socket.gethostname() + ' %(name)-12s %(levelname)-8s %(message)s'
    pixelated_log = logging.FileHandler(LOG_FILE)
    pixelated_log.setLevel(logging.DEBUG)
    pixelated_log.setFormatter(logging.Formatter(pixelated_log_format))

    logging.getLogger('').addHandler(pixelated_log)
    init_twisted_logging()
    debug_enabled = args.debug or os.environ.get('DEBUG', False)

    if debug_enabled:
        init_debugger()


def init_debugger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename='/tmp/leap.log',
                        filemode='w')  # define a Handler which writes INFO messages or higher to the sys.stderr

    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def init_twisted_logging():
    log.startLogging(sys.stdout)
    file_observer = PixelatedLogObserver(file(LOG_FILE, 'a'))
    log.addObserver(file_observer.emit)


class PixelatedLogObserver(log.FileLogObserver):

    """ FileLogObserver with a customized format """
    def emit(self, event):
        text = log.textFromEventDict(event)

        if text is None:
            return

        self.timeFormat = '[%Y-%m-%d %H:%M:%S]'
        time_str = self.formatTime(event['time'])

        fmt_dict = {'text': text.replace('\n', '\n\t')}
        msg_str = log._safeFormat('%(text)s\n', fmt_dict)

        logging.debug(str(event))

        util.untilConcludes(self.write, time_str + ' ' + socket.gethostname() + ' ' + msg_str)
        util.untilConcludes(self.flush)
