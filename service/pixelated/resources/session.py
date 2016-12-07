#
# Copyright (c) 2016 ThoughtWorks, Inc.
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
import hashlib
import os

from zope.interface import Interface, Attribute, implements
from twisted.python.components import registerAdapter
from twisted.web.server import Session

CSRF_TOKEN_LENGTH = 32


class IPixelatedSession(Interface):
    user_uuid = Attribute('The uuid of the currently logged in user')


class PixelatedSession(object):
    implements(IPixelatedSession)

    def __init__(self, session):
        self.user_uuid = None
        self._csrf_token = None

    def is_logged_in(self):
        return self.user_uuid is not None

    def expire(self):
        self.user_uuid = None

    def get_csrf_token(self):
        if self._csrf_token is None:
            self._csrf_token = hashlib.sha256(os.urandom(CSRF_TOKEN_LENGTH)).hexdigest()
        return self._csrf_token


registerAdapter(PixelatedSession, Session, IPixelatedSession)
