import os
from os.path import expanduser
from distutils.spawn import find_executable


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

    def __init__(self, leap_home=DEFAULT_LEAP_HOME, ca_cert_bundle=AUTO_DETECT_CA_BUNDLE, verify_ssl=True,
                 fetch_interval_in_s=30,
                 timeout_in_s=15, start_background_jobs=True, gpg_binary=discover_gpg_binary()):
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
        self.ca_cert_bundle = ca_cert_bundle
        self.verify_ssl = verify_ssl
        self.timeout_in_s = timeout_in_s
        self.start_background_jobs = start_background_jobs
        self.gpg_binary = gpg_binary
        self.fetch_interval_in_s = fetch_interval_in_s
