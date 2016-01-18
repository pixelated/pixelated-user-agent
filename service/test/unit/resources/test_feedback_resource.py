import json
from mockito import verify, mock, when, any as ANY
from twisted.trial import unittest
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.feedback_resource import FeedbackResource
from test.unit.resources import DummySite


class TestFeedbackResource(unittest.TestCase):
    def setUp(self):
        self.feedback_service = mock()
        self.servicesFactory = mock()
        self.services = mock()
        self.services.feedback_service = self.feedback_service
        self.servicesFactory._services_by_user = {'someuserid': self.feedback_service}
        when(self.servicesFactory).services(ANY()).thenReturn(self.services)

        self.web = DummySite(FeedbackResource(self.servicesFactory))

    def test_sends_feedback_to_leap_web(self):
        request = DummyRequest(['/feedback'])
        request.method = 'POST'
        content = mock()
        when(content).read().thenReturn(json.dumps({'feedback': 'Pixelated is awesome!'}))
        request.content = content

        d = self.web.get(request)

        def assert_posted_feedback_to_leap_web(_):
            verify(self.feedback_service).open_ticket('Pixelated is awesome!')

        d.addCallback(assert_posted_feedback_to_leap_web)
        return d
