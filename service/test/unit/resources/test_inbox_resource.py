import re

from mock import MagicMock, patch
from mockito import mock, when, any as ANY

from pixelated.application import UserAgentMode
from pixelated.resources.features_resource import FeaturesResource
from test.unit.resources import DummySite
from twisted.trial import unittest
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.inbox_resource import InboxResource, MODE_STARTUP, MODE_RUNNING


class TestInboxResource(unittest.TestCase):
    MAIL_ADDRESS = 'test_user@pixelated-project.org'

    def setUp(self):
        mail_service = mock()
        mail_service.account_email = self.MAIL_ADDRESS

        services = mock()
        services.mail_service = mail_service

        services_factory = mock()
        services_factory.mode = mock()
        when(services_factory).services(ANY()).thenReturn(services)

        self.inbox_resource = InboxResource(services_factory)
        self.web = DummySite(self.inbox_resource)

    def test_render_GET_should_template_account_email(self):
        self.inbox_resource._html_template = "<html><head><title>$account_email</title></head></html>"
        self.inbox_resource.initialize()

        request = DummyRequest([''])
        request.addCookie = lambda key, value: 'stubbed'

        d = self.web.get(request)

        def assert_response(_):
            expected = "<title>{0}</title>".format(self.MAIL_ADDRESS)
            matches = re.findall(expected, request.written[0])
            self.assertEquals(len(matches), 1)

        d.addCallback(assert_response)
        return d
