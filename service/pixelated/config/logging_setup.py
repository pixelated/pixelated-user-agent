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
import os
from twisted.python import log


def init_logging(debug=False):
    debug_enabled = debug or os.environ.get('DEBUG', False)
    logging_level = logging.DEBUG if debug_enabled else logging.INFO
    log_format = "%(asctime)s [%(name)s] %(levelname)s %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(level=logging_level,
                        format=log_format,
                        datefmt=date_format,
                        filemode='a')

    observer = log.PythonLoggingObserver()
    observer.start()
