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
import getpass
import logging
import pixelated.bitmask_libraries.session as LeapSession
from pixelated.bitmask_libraries.certs import which_api_CA_bundle
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.provider import LeapProvider
from leap.auth import SRPAuth

logger = logging.getLogger(__name__)


def register(server_name, username):
    try:
        validate_username(username)
    except ValueError:
        print('Only lowercase letters, digits, . - and _ allowed.')

    config = LeapConfig()
    provider = LeapProvider(server_name, config)
    password = getpass.getpass('Please enter password for %s: ' % username)
    srp_auth = SRPAuth(provider.api_uri, which_api_CA_bundle(provider))

    if srp_auth.register(username, password):
        session = LeapSession.open(username, password, server_name)
        session.nicknym.generate_openpgp_key()
    else:
        logger.error("Register failed")


def validate_username(username):
    accepted_characters = '^[a-z0-9\-\_\.]*$'
    if not re.match(accepted_characters, username):
        raise ValueError
