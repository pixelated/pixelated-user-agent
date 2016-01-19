import unittest
import re
from mockito import mock, when, any as ANY
from test.unit.resources import DummySite
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.root_resource import RootResource


class TestRootResource(unittest.TestCase):
    MAIL_ADDRESS = 'test_user@pixelated-project.org'

    def setUp(self):
        self.services_factory_mock = mock()
        self.mail_service_mock = mock()
        root_resource = RootResource(self.services_factory_mock)
        root_resource._mode = root_resource
        root_resource.account_email = self.MAIL_ADDRESS
        root_resource._html_template = "<html><head><title>$account_email</title></head></html>"
        self.web = DummySite(root_resource)

    def test_render_GET_should_template_account_email(self):
        when(self.services_factory_mock).mail_service(ANY()).thenReturn(self.mail_service_mock)
        self.mail_service_mock.account_email = self.MAIL_ADDRESS
        request = DummyRequest([''])

        d = self.web.get(request)

        def assert_response(_):
            expected = "<title>{0}</title>".format(self.MAIL_ADDRESS)
            matches = re.findall(expected, request.written[0])
            self.assertEquals(len(matches), 1)

        d.addCallback(assert_response)
        return d
