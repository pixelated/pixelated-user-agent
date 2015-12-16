import json
import unittest

from mock import patch, MagicMock
from twisted.internet import defer
from twisted.web.test.requesthelper import DummyRequest

from pixelated.resources.attachments_resource import AttachmentsResource
from test.unit.resources import DummySite


class AttachmentsResourceTest(unittest.TestCase):

    def setUp(self):
        self.mail_service = MagicMock()
        self.mails_resource = AttachmentsResource(self.mail_service)
        self.mails_resource.isLeaf = True
        self.web = DummySite(self.mails_resource)

    @patch('twisted.internet.defer.maybeDeferred')
    @patch('cgi.FieldStorage')
    def test_post_new_attachment(self, mock_fields, mock_maybe_deferred):
        request = DummyRequest(['/attachment'])
        request.method = 'POST'
        request.content = 'mocked'
        attachment_id = 'B5B4ED80AC3B894523D72E375DACAA2FC6606C18EDF680FE95903086C8B5E14A'
        mock_maybe_deferred.return_value = defer.succeed(attachment_id)

        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(201, request.code)
            self.assertEqual('/attachment/%s' % attachment_id, request.headers['Location'])
            self.assertEqual({'attachment_id': attachment_id}, json.loads(request.written[0]))

        d.addCallback(assert_response)
        return d

    @patch('twisted.internet.defer.maybeDeferred')
    @patch('cgi.FieldStorage')
    def test_post_attachment_fails(self, mock_fields, mock_maybe_deferred):
        mock_maybe_deferred.return_value = defer.fail(Exception)
        request = DummyRequest(['/attachment'])
        request.method = 'POST'
        request.content = 'mocked'

        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(500, request.code)
            self.assertFalse('Location' in request.headers)
            self.assertEqual({"message": "Something went wrong. Attachement not saved."}, json.loads(request.written[0]))

        d.addCallback(assert_response)
        return d
