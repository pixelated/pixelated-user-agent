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
from mock import patch
from unittest import skip
from pixelated.bitmask_libraries.soledad import SoledadSession
from test_abstract_leap import AbstractLeapTest


@patch('pixelated.bitmask_libraries.soledad.Soledad')
class SoledadSessionTest(AbstractLeapTest):

    def setUp(self):
        super(SoledadSessionTest, self).setUp()

        # given
        self.provider.fetch_soledad_json.return_value = {'hosts': {
            'couch1': {
                'hostname': 'couch1.some-server.test',
                'ip_address': '192.168.1.1',
                'port': 1234
            }
        }}

    @patch('pixelated.bitmask_libraries.soledad.Soledad.__init__')
    def test_that_soledad_is_created_with_required_params(self, soledad_mock, init_mock):
        # when
        SoledadSession(self.provider, 'any-passphrase', self.auth.token, self.auth.uuid)

        # then
        init_mock.assert_called_with(self.auth.uuid, 'any-passphrase', '%s/soledad/%s.secret' % (self.leap_home, self.auth.uuid),
                                     '%s/soledad/%s.db' % (self.leap_home, self.auth.uuid),
                                     'https://couch1.some-server.test:1234/user-%s' % self.auth.uuid,
                                     '/some/path/to/ca_cert', self.token, defer_encryption=False)

    def test_that_sync_is_called(self, soledad_mock):
            instance = soledad_mock.return_value
            instance.server_url = '/foo/bar'
            soledad_session = SoledadSession(self.provider, 'any-passphrase', self.auth.token, self.auth.uuid)

            # when
            soledad_session.sync()

            # then
            instance.sync.assert_called_with()

    @skip("need_sync is gone, we need to find out what can replace it")
    def test_that_sync_not_called_if_not_needed(self, mock):
            instance = mock.return_value
            instance.server_url = '/foo/bar'
            instance.need_sync.return_value = False
            soledad_session = SoledadSession(self.provider, 'any-passphrase', self.auth.token, self.auth.uuid)

            # when
            soledad_session.sync()

            # then
            instance.need_sync.assert_called_with('/foo/bar')
            self.assertFalse(instance.sync.called)
