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


class PrivateKeyFilter(logging.Filter):

    def filter(self, record):
        if '-----BEGIN PGP PRIVATE KEY BLOCK-----' in record.msg:
            record.msg = '*** private key removed by %s.%s ***' % (type(self).__module__, type(self).__name__)
        return True


def init(debug=False):
    debug_enabled = debug or os.environ.get('DEBUG', False)
    logging_level = logging.DEBUG if debug_enabled else logging.INFO

    logging.basicConfig(level=logging_level,
                        format='%(asctime)s [%(name)s] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filemode='a')

    logging.getLogger('gnupg').addFilter(PrivateKeyFilter())

    observer = log.PythonLoggingObserver()
    observer.start()
