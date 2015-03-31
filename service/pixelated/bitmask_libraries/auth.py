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
from .leap_srp import LeapSecureRemotePassword
from .certs import which_api_CA_bundle

USE_PASSWORD = None


class LeapCredentials(object):
    def __init__(self, user_name, password, db_passphrase=USE_PASSWORD):
        self.user_name = user_name
        self.password = password
        self.db_passphrase = db_passphrase if db_passphrase is not None else password


class LeapAuthenticator(object):
    def __init__(self, provider):
        self._provider = provider

    def authenticate(self, credentials):
        config = self._provider.config
        srp = LeapSecureRemotePassword(ca_bundle=which_api_CA_bundle(self._provider), timeout_in_s=config.timeout_in_s)
        srp_session = srp.authenticate(self._provider.api_uri, credentials.user_name, credentials.password)
        return srp_session

    def register(self, credentials):
        config = self._provider.config
        srp = LeapSecureRemotePassword(ca_bundle=which_api_CA_bundle(self._provider), timeout_in_s=config.timeout_in_s)
        srp.register(self._provider.api_uri, credentials.user_name, credentials.password)
