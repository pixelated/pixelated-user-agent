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
import os
import requests
import random
from leap.mail.smtp import setup_smtp_gateway
from pixelated.bitmask_libraries.certs import LeapCertificate


logger = logging.getLogger(__name__)


class LeapSmtp(object):

    def __init__(self, provider, auth, keymanager=None):
        self.local_smtp_port_number = random.randrange(12000, 16000)
        self._provider = provider
        self.username = auth.username
        self.session_id = auth.session_id
        self.user_token = auth.token
        self._keymanager = keymanager
        self._remote_hostname, self._remote_port = provider.smtp_info()
        self._local_smtp_service_socket = None
        self._local_smtp_service = None

    def start(self):
        cert_path = self._provider._client_cert_path()
        email = '%s@%s' % (self.username, self._provider.domain)

        self._local_smtp_service, self._local_smtp_service_socket = setup_smtp_gateway(
            port=self.local_smtp_port_number,
            userid=str(email),
            keymanager=self._keymanager,
            smtp_host=self._remote_hostname.encode('UTF-8'),
            smtp_port=self._remote_port,
            smtp_cert=cert_path,
            smtp_key=cert_path,
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
