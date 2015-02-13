import json
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

        def assert_response(_):
            self.assertEquals('"{\\"tags\\": [\\"keymanager-key\\"], \\"fingerprint\\": null, '
                              '\\"private\\": null, \\"expiry_date\\": null, \\"address\\": '
                              '\\"some@key\\", \\"last_audited_at\\": null, \\"key_data\\": null, '
                              '\\"length\\": null, \\"key_id\\": null, \\"validation\\": null, '
                              '\\"type\\": \\"<class \'leap.keymanager.openpgp.OpenPGPKey\'>\\", '
                              '\\"first_seen_at\\": null}"', request.written[0])

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
