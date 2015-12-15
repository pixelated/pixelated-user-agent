import json
import os
import unittest

from mock import patch
from mockito import mock, when, verify
from twisted.internet import defer
from twisted.web.test.requesthelper import DummyRequest

from pixelated.resources.attachments_resource import AttachmentsResource
from pixelated.resources.features_resource import FeaturesResource
from test.unit.resources import DummySite


class FeatureResourceTest(unittest.TestCase):

    def setUp(self):
        self.feature_resource = FeaturesResource()
        self.web = DummySite(self.feature_resource)

    def test_attachment_feature_is_disabled(self):
        request = DummyRequest(['/features'])

        with patch.dict(os.environ, {}, clear=True):
            self.web.get(request)

        self.assertEqual(200, request.code)

        response = json.loads(request.written[0])
        self.assertTrue('attachment' in response['disabled_features'])

    def test_attachment_feature_is_enabled(self):
        request = DummyRequest(['/features'])

        with patch.dict(os.environ, {'ATTACHMENT': 'Not empty'}, clear=True):
            self.web.get(request)

        self.assertEqual(200, request.code)

        response = json.loads(request.written[0])
        self.assertFalse('attachment' in response['disabled_features'])
