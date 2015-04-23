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

import getpass

import os
import os.path
import pixelated.bitmask_libraries.session as LeapSession
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.provider import LeapProvider
from leap.srp_auth import SRPAuth


def register_new_user(username, server_name):
    config = LeapConfig()
    provider = LeapProvider(server_name, config)
    password = getpass.getpass('Please enter password for %s: ' % username)
    srp_auth = SRPAuth(provider, provider.local_ca_crt)
    srp_auth.register(username, password)

    session = LeapSession.open(username, password, server_name)
    session.nicknym.generate_openpgp_key()
