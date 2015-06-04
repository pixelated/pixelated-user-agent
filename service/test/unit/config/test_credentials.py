import json
import unittest
import sys
from mockito import mock, when
from pixelated.config.args import parse_user_agent_args
from pixelated.config import credentials


class TestReadCredentials(unittest.TestCase):

    def setUp(self):
        self.test_data = {'leap_provider_hostname': 'test_provider', 'user': 'test_user', 'password': 'test_password'}

    def test_organization_mode_reads_credentials_from_stdin(self):
        data = json.dumps({'leap_provider_hostname': 'test_provider', 'user': 'test_user', 'password': 'test_password'})
        orig_stdin = sys.stdin
        sys.stdin = mock()
        when(sys.stdin).read().thenReturn(data)

        try:
            sys.argv = ['tmp/does_not_exist', '--organization-mode']
            args = parse_user_agent_args()

            provider, user, password = credentials.read(args.organization_mode, 'not_used')

            self.assertEquals('test_provider', provider)
            self.assertEquals('test_user', user)
            self.assertEquals('test_password', password)
        finally:
            sys.stdin = orig_stdin
