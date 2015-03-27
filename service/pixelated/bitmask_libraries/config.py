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
from distutils.spawn import find_executable

import os
from os.path import expanduser


def discover_gpg_binary():
    path = find_executable('gpg')
    if path is None:
        raise Exception('Did not find a gpg executable!')

    if os.path.islink(path):
        path = os.path.realpath(path)

    return path


DEFAULT_LEAP_HOME = os.path.join(expanduser("~"), '.leap')

SYSTEM_CA_BUNDLE = True
AUTO_DETECT_CA_BUNDLE = None


class LeapConfig(object):
    """
    LEAP client configuration

    """

    def __init__(self, leap_home=DEFAULT_LEAP_HOME, bootstrap_ca_cert_bundle=AUTO_DETECT_CA_BUNDLE,
                 ca_cert_bundle=AUTO_DETECT_CA_BUNDLE, verify_ssl=True,
                 fetch_interval_in_s=30,
                 timeout_in_s=15, start_background_jobs=False, gpg_binary=discover_gpg_binary(), certs_home=None):
        """
        Constructor.

        :param server_name: The LEAP server name, e.g. demo.leap.se
        :type server_name: str

        :param user_name: The LEAP account user name, normally the first part of your email, e.g. foobar for foobar@demo.leap.se
        :type user_name: str

        :param user_password: The LEAP account password
        :type user_password: str

        :param db_passphrase: The passphrase used to encrypt the local soledad database
        :type db_passphrase: str

        :param verify_ssl: Set to false to disable strict SSL certificate validation
        :type verify_ssl: bool

        :param fetch_interval_in_s: Polling interval for fetching incoming mail from LEAP server
        :type fetch_interval_in_s: int

        :param timeout_in_s: Timeout for network operations, e.g. HTTP calls
        :type timeout_in_s: int

        :param gpg_binary: Path to the GPG binary (must not be a symlink)
        :type gpg_binary: str

        """
        self.leap_home = leap_home
        self.certs_home = certs_home
        self.bootstrap_ca_cert_bundle = bootstrap_ca_cert_bundle
        self.ca_cert_bundle = ca_cert_bundle
        self.verify_ssl = verify_ssl
        self.timeout_in_s = timeout_in_s
        self.start_background_jobs = start_background_jobs
        self.gpg_binary = gpg_binary
        self.fetch_interval_in_s = fetch_interval_in_s
