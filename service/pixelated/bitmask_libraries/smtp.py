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
import logging
import random
from leap.mail.smtp import setup_smtp_gateway


logger = logging.getLogger(__name__)


class LeapSMTPConfig(object):

    def __init__(self, account_email, cert_path, remote_smtp_host, remote_smtp_port):
        self.account_email = account_email
        self.cert_path = cert_path
        self.remote_smtp_host = remote_smtp_host
        self.remote_smtp_port = remote_smtp_port


class LeapSmtp(object):

    def __init__(self, smtp_config, keymanager=None):
        self.local_smtp_port_number = random.randrange(12000, 16000)
        self._smtp_config = smtp_config
        self._keymanager = keymanager
        self._local_smtp_service_socket = None
        self._local_smtp_service = None

    def start(self):
        self._local_smtp_service, self._local_smtp_service_socket = setup_smtp_gateway(
            port=self.local_smtp_port_number,
            userid=str(self._smtp_config.account_email),
            keymanager=self._keymanager,
            smtp_host=self._smtp_config.remote_smtp_host.encode('UTF-8'),
            smtp_port=self._smtp_config.remote_smtp_port,
            smtp_cert=self._smtp_config.cert_path,
            smtp_key=self._smtp_config.cert_path,
            encrypted_only=False
        )

    def ensure_running(self):
        if not self._local_smtp_service:
            try:
                self.start()
            except:
                logger.warning("Couldn't start the SMTP server now, will try again when the user tries to use it")
                return False
        return True

    def stop(self):
        if self._local_smtp_service is not None:
            self._local_smtp_service_socket.stopListening()
            self._local_smtp_service.doStop()
            self._local_smtp_service_socket = None
            self._local_smtp_service = None
