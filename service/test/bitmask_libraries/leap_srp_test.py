import json
import unittest
import binascii
from urlparse import parse_qs

from httmock import urlmatch, all_requests, HTTMock, response
from requests.exceptions import Timeout
import srp

from app.bitmask_libraries.leap_srp import LeapSecureRemotePassword, LeapAuthException



(salt_bytes, verification_key_bytes) =  srp.create_salted_verification_key('username', 'password', hash_alg=srp.SHA256, ng_type=srp.NG_1024)
verifier = None


@all_requests
def not_found_mock(url, request):
    return {'status_code': 404,
                'content': 'foobar'}


@all_requests
def timeout_mock(url, request):
    raise Timeout()

@urlmatch(netloc=r'(.*\.)?leap\.local$')
def srp_login_server_simulator_mock(url, request):
    global verifier

    data = parse_qs(request.body)
    if 'login' in data:
        # SRP Authentication Step 1
        A = binascii.unhexlify(data.get('A')[0])

        verifier = srp.Verifier('username', salt_bytes, verification_key_bytes, A, hash_alg=srp.SHA256, ng_type=srp.NG_1024)
        (salt, B) = verifier.get_challenge()

        content = {
            'salt': binascii.hexlify(salt),
            'B': binascii.hexlify(B)
        }

        return {'status_code': 200,
                'content': json.dumps(content)}

    else:
        # SRP Authentication Step 2
        data = parse_qs(request.body)
        client_auth = binascii.unhexlify(data.get('client_auth')[0])

        M2 = verifier.verify_session(client_auth)

        if not verifier.authenticated():
            return {'status_code': 404,
                    'content': ''}

        content = {
            'M2': binascii.hexlify(M2),
            'id': 'some id',
            'token': 'some token'
        }
        headers = {
            'Content-Type': 'application/json',
            'Set-Cookie': '_session_id=some_session_id;'}
        return response(200, content, headers, None, 5, request)


class LeapSRPTest(unittest.TestCase):

    def test_status_code_is_checked(self):
        with HTTMock(not_found_mock):
            lsrp = LeapSecureRemotePassword()
            self.assertRaises(LeapAuthException, lsrp.authenticate, 'https://api.leap.local', 'username', 'password')

    def test_invalid_username(self):
        with HTTMock(srp_login_server_simulator_mock):
            lsrp = LeapSecureRemotePassword()
            self.assertRaises(LeapAuthException, lsrp.authenticate, 'https://api.leap.local', 'invalid_user', 'password')

    def test_invalid_password(self):
        with HTTMock(srp_login_server_simulator_mock):
            lsrp = LeapSecureRemotePassword()
            self.assertRaises(LeapAuthException, lsrp.authenticate, 'https://api.leap.local', 'username', 'invalid')

    def test_login(self):
        with HTTMock(srp_login_server_simulator_mock):
            lsrp = LeapSecureRemotePassword()
            leap_session = lsrp.authenticate('https://api.leap.local', 'username', 'password')

            self.assertIsNotNone(leap_session)
            self.assertEqual('username', leap_session.user_name)
            self.assertEqual('1', leap_session.api_version)
            self.assertEqual('https://api.leap.local', leap_session.api_server_name)
            self.assertEqual('some token', leap_session.token)
            self.assertEqual('some_session_id', leap_session.session_id)

    def test_timeout(self):
        with HTTMock(timeout_mock):
            lrsp = LeapSecureRemotePassword()
            self.assertRaises(LeapAuthException, lrsp.authenticate, 'https://api.leap.local', 'username', 'password')
