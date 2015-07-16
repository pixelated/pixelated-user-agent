import json
import ast
from mockito import mock, when
from leap.keymanager import OpenPGPKey, KeyNotFound
from pixelated.resources.keys_resource import KeysResource
import twisted.trial.unittest as unittest
from twisted.web.test.requesthelper import DummyRequest
from test.unit.resources import DummySite


class TestKeysResource(unittest.TestCase):

    def setUp(self):
        self.keymanager = mock()
        self.web = DummySite(KeysResource(self.keymanager))

    def test_returns_404_if_key_not_found(self):
        request = DummyRequest(['/keys'])
        request.addArg('search', 'some@inexistent.key')
        when(self.keymanager).get_key_from_cache('some@inexistent.key', OpenPGPKey).thenRaise(KeyNotFound())

        d = self.web.get(request)

        def assert_404(_):
            self.assertEquals(404, request.code)

        d.addCallback(assert_404)
        return d

    def test_returns_the_key_as_json_if_found(self):
        request = DummyRequest(['/keys'])
        request.addArg('search', 'some@key')
        when(self.keymanager).get_key_from_cache('some@key', OpenPGPKey).thenReturn(OpenPGPKey('some@key'))

        d = self.web.get(request)

        expected = {
            "tags": ["keymanager-key"],
            "fingerprint": '',
            "private": False,
            'sign_used': False,
            'refreshed_at': 0,
            "expiry_date": 0,
            "address": 'some@key',
            'encr_used': False,
            'last_audited_at': 0,
            'key_data': '',
            'length': 0,
            'key_id': '',
            'validation': 'Weak_Chain',
            'type': 'OpenPGPKey',
        }

        def assert_response(_):
            actual = json.loads(ast.literal_eval(request.written[0]))
            self.assertEquals(expected, actual)

        d.addCallback(assert_response)
        return d

    def test_returns_unauthorized_if_key_is_private(self):
        request = DummyRequest(['/keys'])
        request.addArg('search', 'some@key')
        when(self.keymanager).get_key_from_cache('some@key', OpenPGPKey).thenReturn(OpenPGPKey('some@key', private=True))

        d = self.web.get(request)

        def assert_response(_):
            self.assertEquals(401, request.code)

        d.addCallback(assert_response)
        return d
