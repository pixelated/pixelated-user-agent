import json
import unittest

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

    def test_post_new_attachment(self):
        request = DummyRequest(['/attachment'])
        request.method = 'POST'
        attachment = 'some fake file'
        request.args = {'attachment': [attachment,]}
        attachment_id = 'B5B4ED80AC3B894523D72E375DACAA2FC6606C18EDF680FE95903086C8B5E14A'

        when(self.mail_service).attachment_id(attachment).thenReturn(defer.succeed(attachment_id))

        d = self.web.get(request)

        def assert_response(_):
            verify(self.mail_service).attachment_id(attachment)
            self.assertEqual(201, request.code)
            self.assertEqual('/attachment/%s' % attachment_id, request.headers['Location'])
            self.assertEqual({'attachment_id': attachment_id}, json.loads(request.written[0]))

        d.addCallback(assert_response)
        return d

    def test_post_attachment_fails(self):
        request = DummyRequest(['/attachment'])
        request.method = 'POST'
        attachment = 'some fake file'
        request.args = {'attachment': [attachment,]}

        when(self.mail_service).attachment_id(attachment).thenReturn(defer.fail(Exception))

        d = self.web.get(request)

        def assert_response(_):
            self.assertEqual(500, request.code)
            self.assertFalse('Location' in request.headers)
            verify(self.mail_service).attachment_id(attachment)
            self.assertEqual({"message": "Something went wrong. Attachement not saved."}, json.loads(request.written[0]))

        d.addCallback(assert_response)
        return d