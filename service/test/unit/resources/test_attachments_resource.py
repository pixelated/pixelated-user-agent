import json
import unittest

from mock import patch, MagicMock
from mockito import mock, when, verify
from twisted.internet import defer
from twisted.web.test.requesthelper import DummyRequest

from pixelated.resources.attachments_resource import AttachmentsResource
from test.unit.resources import DummySite


class AttachmentsResourceTest(unittest.TestCase):

    def setUp(self):
        self.mail_service = mock()
        self.mails_resource = AttachmentsResource(self.mail_service)
        self.mails_resource.isLeaf = True
        self.web = DummySite(self.mails_resource)

    @patch('cgi.FieldStorage')
    def test_post_new_attachment(self, mock_fields):
        request = DummyRequest(['/attachment'])
        request.method = 'POST'
        request.content = 'mocked'
        attachment_id = 'B5B4ED80AC3B894523D72E375DACAA2FC6606C18EDF680FE95903086C8B5E14A'
        _file = MagicMock()
        _file.value = 'some mocked value'
        _file.type = 'some mocked type'
        _file.filename = 'filename.txt'
        mock_fields.return_value = {'attachment': _file}
        when(self.mail_service).save_attachment('some mocked value', 'some mocked type').thenReturn(defer.succeed(attachment_id))

        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(201, request.code)
            self.assertEqual('/attachment/%s' % attachment_id, request.headers['Location'])
            response_json = {'attachment_id': attachment_id, 'content-type': 'some mocked type',
                             'filename': 'filename.txt', 'filesize': 17}
            self.assertEqual(response_json, json.loads(request.written[0]))
            verify(self.mail_service).save_attachment('some mocked value', 'some mocked type')

        d.addCallback(assert_response)
        return d

    @patch('cgi.FieldStorage')
    def test_post_attachment_fails(self, mock_fields):
        request = DummyRequest(['/attachment'])
        request.method = 'POST'
        request.content = 'mocked'

        _file = MagicMock()
        _file.value = 'some mocked value'
        _file.type = 'some mocked type'
        mock_fields.return_value = {'attachment': _file}
        when(self.mail_service).save_attachment('some mocked value', 'some mocked type').thenReturn(defer.fail(Exception))

        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(500, request.code)
            self.assertFalse('Location' in request.headers)
            self.assertEqual({"message": "Something went wrong. Attachement not saved."}, json.loads(request.written[0]))
            verify(self.mail_service).save_attachment('some mocked value', 'some mocked type')

        d.addCallback(assert_response)
        return d
