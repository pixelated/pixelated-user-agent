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
import leap.keymanager
import requests
import logging
from leap.keymanager.errors import KeyNotFound


logger = logging.getLogger(__name__)


def patched_fetch_keys_from_server(self, address):
        """
        Fetch keys bound to C{address} from nickserver and insert them in
        local database.

        Instead of raising a KeyNotFound only for 404 responses, this implementation
        raises a KeyNotFound exception for all problems.

        For original see: https://github.com/leapcode/keymanager/blob/develop/src/leap/keymanager/__init__.py

        :param address: The address bound to the keys.
        :type address: str

        :raise KeyNotFound: If the key was not found on nickserver.
        """
        # request keys from the nickserver
        res = None
        try:
            res = self._get(self._nickserver_uri, {'address': address})
            res.raise_for_status()
            server_keys = res.json()
            # insert keys in local database
            if self.OPENPGP_KEY in server_keys:
                self._wrapper_map[OpenPGPKey].put_ascii_key(
                    server_keys['openpgp'])
        except requests.exceptions.HTTPError as e:
            logger.warning("HTTP error retrieving key: %r" % (e,))
            logger.warning("%s" % (res.content,))
            raise KeyNotFound(address)
        except Exception as e:
            logger.warning("Error retrieving key: %r" % (e,))
            raise KeyNotFound(address)


leap.keymanager.KeyManager._fetch_keys_from_server = patched_fetch_keys_from_server
