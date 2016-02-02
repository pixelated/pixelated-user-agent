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
import time
import logging
from functools import wraps
from twisted.internet import defer


log = logging.getLogger(__name__)


def log_time(f):

    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.clock()
        result = f(*args, **kwds)
        log.info('Needed %f ms to execute %s' % ((time.clock() - start), f))

        return result

    return wrapper


def log_time_deferred(f):

    def log_time(result, start):
        log.info('after callback: Needed %f ms to execute %s' % ((time.clock() - start), f))
        return result

    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.clock()
        result = f(*args, **kwds)
        if isinstance(result, defer.Deferred):
            result.addCallback(log_time, start=start)
        else:
            log.warn('No Deferred returned, perhaps need to re-order annotations?')
        return result

    return wrapper
