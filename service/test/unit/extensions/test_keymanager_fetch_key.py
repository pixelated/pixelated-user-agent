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
import unittest
from mock import MagicMock, patch

from leap.keymanager import KeyManager
from leap.keymanager.keys import KEY_ADDRESS_KEY, KEY_TYPE_KEY, KEY_ID_KEY, KEY_FINGERPRINT_KEY, KEY_DATA_KEY, KEY_PRIVATE_KEY, KEY_LENGTH_KEY, KEY_EXPIRY_DATE_KEY, KEY_FIRST_SEEN_AT_KEY, KEY_LAST_AUDITED_AT_KEY, KEY_VALIDATION_KEY, KEY_TAGS_KEY
from leap.keymanager.openpgp import OpenPGPKey
from leap.keymanager.errors import KeyNotFound
from requests.exceptions import HTTPError


class TestDoc(object):
    def __init__(self, encryption_key):
        self.content = encryption_key

sample_key = {
    KEY_ADDRESS_KEY: 'foo@bar.de',
    KEY_TYPE_KEY: 'type',
    KEY_ID_KEY: 'key_id',
    KEY_FINGERPRINT_KEY: 'fingerprint',
    KEY_DATA_KEY: 'key_data',
    KEY_PRIVATE_KEY: None,
    KEY_LENGTH_KEY: 'length',
    KEY_EXPIRY_DATE_KEY: 'expiry_date',
    KEY_FIRST_SEEN_AT_KEY: 'first_seen_at',
    KEY_LAST_AUDITED_AT_KEY: 'last_audited_at',
    KEY_VALIDATION_KEY: 'validation',
    KEY_TAGS_KEY: 'tags',
}


class TestExtKeyManagerFetchKey(unittest.TestCase):

    @patch('leap.keymanager.requests')
    def test_retrieves_key(self, requests_mock):
        nickserver_url = 'http://some/nickserver/uri'
        soledad = MagicMock()
        soledad.get_from_index.side_effect = [[], [TestDoc(sample_key)]]

        km = KeyManager('me@bar.de', nickserver_url, soledad, ca_cert_path='some path')

        result = km.get_key('foo@bar.de', OpenPGPKey)

        self.assertEqual(str(OpenPGPKey('foo@bar.de', key_id='key_id')), str(result))

    @patch('leap.keymanager.requests')
    def test_http_error_500(self, requests_mock):
        def do_request(one, data=None, verify=None):
            response = MagicMock()
            response.raise_for_status = MagicMock()
            response.raise_for_status.side_effect = HTTPError
            return response

        nickserver_url = 'http://some/nickserver/uri'
        soledad = MagicMock()
        soledad.get_from_index.side_effect = [[], []]
        requests_mock.get.side_effect = do_request

        km = KeyManager('me@bar.de', nickserver_url, soledad, ca_cert_path='some path')

        self.assertRaises(KeyNotFound, km.get_key, 'foo@bar.de', OpenPGPKey)
