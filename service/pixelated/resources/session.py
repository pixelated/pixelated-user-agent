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

from zope.interface import Interface, Attribute, implements
from twisted.python.components import registerAdapter
from twisted.web.server import Session


class IPixelatedSession(Interface):
    user_uuid = Attribute('The uuid of the currently logged in user')
    login_status = Attribute('The status during user login')


class PixelatedSession(object):
    implements(IPixelatedSession)

    def __init__(self, session):
        self.user_uuid = None
        self.login_status = None

    def is_logged_in(self):
        return self.user_uuid is not None

    def expire(self):
        self.user_uuid = None
        self.login_status = None

    def login_started(self):
        self.login_status = 'started'

    def login_completed(self, user_uuid):
        self.user_uuid = user_uuid
        self.login_status = 'completed'

    def login_error(self):
        self.login_status = 'error'

    def check_login_status(self):
        return self.login_status


registerAdapter(PixelatedSession, Session, IPixelatedSession)
