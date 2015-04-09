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
import re

from pixelated.bitmask_libraries.leap_srp import LeapAuthException
from pixelated.bitmask_libraries.register import register_new_user


def register(username, server_name):
    try:
        validate_username(username)
        register_new_user(username, server_name)
    except LeapAuthException:
        print('User already exists')
    except ValueError:
        print('Only lowercase letters, digits, . - and _ allowed.')


def validate_username(username):
    accepted_characters = '^[a-z0-9\-\_]*$'
    if not re.match(accepted_characters, username):
        raise ValueError
