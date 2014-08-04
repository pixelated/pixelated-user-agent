import os
import tempfile
import unittest
from uuid import uuid4
from mock import Mock, MagicMock


class AbstractLeapTest(unittest.TestCase):
    uuid = str(uuid4())
    session_id = str(uuid4())
    token = str(uuid4())

    leap_home = os.path.join(tempfile.mkdtemp(), 'leap')

    config = Mock(leap_home=leap_home, ca_cert_bundle='/some/path/to/ca_cert', gpg_binary='/path/to/gpg')
    provider = Mock(config=config, server_name='some-server.test', domain='some-server.test',
                    api_uri='https://api.some-server.test:4430', api_version='1')
    soledad = Mock()
    soledad_session = Mock(soledad=soledad)
    srp_session = Mock(user_name='test_user', api_server_name='some-server.test', uuid=uuid, session_id=session_id, token=token)

    nicknym = MagicMock()

    soledad_account = MagicMock()

    mail_fetcher_mock = MagicMock()

    def tearDown():
        reload
