from mock import MagicMock
from mockito import mock
from twisted.trial import unittest
from twisted.web.resource import getChildForRequest
from twisted.web.test.requesthelper import DummyRequest

from pixelated.application import get_static_folder
from pixelated.resources.root_resource import RootResource
from pixelated.resources.signup_resource import SignupResource


class TestSignupResource(unittest.TestCase):

    def setUp(self):
        self.public_root_resource = RootResource(mock(), get_static_folder(), public=True)

    def test_get_resource_for_request(self):
        request = DummyRequest(['signup'])
        request.addCookie = MagicMock(return_value='stubbed')
        self.public_root_resource.initialize(provider=mock(), authenticator=mock())
        resource = getChildForRequest(self.public_root_resource, request)

        self.assertIsInstance(resource, SignupResource)
