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
import json

from leap.common.certs import get_digest
import requests
from .certs import which_bootstrap_bundle, which_bundle


class LeapProvider(object):
    def __init__(self, server_name, config):
        self.server_name = server_name
        self.config = config

        self.provider_json = self.fetch_provider_json()

    @property
    def api_uri(self):
        return self.provider_json.get('api_uri')

    @property
    def ca_cert_fingerprint(self):
        return self.provider_json.get('ca_cert_fingerprint')

    @property
    def ca_cert_uri(self):
        return self.provider_json.get('ca_cert_uri')

    @property
    def api_version(self):
        return self.provider_json.get('api_version')

    @property
    def domain(self):
        return self.provider_json.get('domain')

    @property
    def services(self):
        return self.provider_json.get('services')

    def __hash__(self):
        return hash(self.server_name)

    def __eq__(self, other):
        return self.server_name == other.server_name

    def ensure_supports_mx(self):
        if 'mx' not in self.services:
            raise Exception

    def download_certificate_to(self, filename):
        """
        Downloads the server certificate, validates it against the provided fingerprint and stores it to file
        """
        cert = self.fetch_valid_certificate()
        with open(filename, 'w') as out:
            out.write(cert)

    def fetch_valid_certificate(self):
        cert = self._fetch_certificate()
        self.validate_certificate(cert)
        return cert

    def _fetch_certificate(self):
        session = requests.session()
        try:
            cert_url = '%s/ca.crt' % self._provider_base_url()
            response = session.get(cert_url, verify=which_bootstrap_bundle(self), timeout=self.config.timeout_in_s)
            response.raise_for_status()

            cert_data = response.content
            return cert_data
        finally:
            session.close()

    def validate_certificate(self, cert_data=None):
        if cert_data is None:
            cert_data = self._fetch_certificate()

        parts = str(self.ca_cert_fingerprint).split(':')
        method = parts[0].strip()
        fingerprint = parts[1].strip()

        digest = get_digest(cert_data, method)

        if fingerprint.strip() != digest:
            raise Exception('Certificate fingerprints don\'t match')

    def fetch_provider_json(self):
        url = '%s/provider.json' % self._provider_base_url()
        response = requests.get(url, verify=which_bootstrap_bundle(self), timeout=self.config.timeout_in_s)
        response.raise_for_status()

        json_data = json.loads(response.content)
        return json_data

    def fetch_soledad_json(self):
        service_url = "%s/%s/config/soledad-service.json" % (
            self.api_uri, self.api_version)
        response = requests.get(service_url, verify=which_bundle(self), timeout=self.config.timeout_in_s)
        response.raise_for_status()
        return json.loads(response.content)

    def fetch_smtp_json(self):
        service_url = '%s/%s/config/smtp-service.json' % (
            self.api_uri, self.api_version)
        response = requests.get(service_url, verify=which_bundle(self), timeout=self.config.timeout_in_s)
        response.raise_for_status()
        return json.loads(response.content)

    def _provider_base_url(self):
        return 'https://%s' % self.server_name
