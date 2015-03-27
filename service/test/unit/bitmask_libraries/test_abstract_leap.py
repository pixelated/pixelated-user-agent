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
import tempfile
import unittest
from uuid import uuid4

import os
from mock import Mock, MagicMock


class AbstractLeapTest(unittest.TestCase):
    uuid = str(uuid4())
    session_id = str(uuid4())
    token = str(uuid4())

    leap_home = os.path.join(tempfile.mkdtemp(), 'leap')

    config = Mock(leap_home=leap_home, bootstrap_ca_cert_bundle='/some/path/to/ca_cert', ca_cert_bundle='/some/path/to/provider_ca_cert', gpg_binary='/path/to/gpg')
    provider = Mock(config=config, server_name='some-server.test', domain='some-server.test',
                    api_uri='https://api.some-server.test:4430', api_version='1')
    soledad = Mock()
    soledad_session = Mock(soledad=soledad)
    srp_session = Mock(user_name='test_user', api_server_name='some-server.test', uuid=uuid, session_id=session_id, token=token)

    nicknym = MagicMock()

    soledad_account = MagicMock()

    mail_fetcher_mock = MagicMock()
