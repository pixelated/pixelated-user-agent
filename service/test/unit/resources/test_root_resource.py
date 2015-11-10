import unittest
from mockito import mock, when
from test.unit.resources import DummySite
from twisted.web.test.requesthelper import DummyRequest
from pixelated.resources.root_resource import RootResource


class TestRootResource(unittest.TestCase):

    def setUp(self):
        test_email = 'hackerman@pixelated-project.org'
        mail_service = mock()
        mail_service.account_email = test_email

        root_resource = RootResource()
        root_resource.initialize(mock(), mock(), mail_service, mock(), mock())
        root_resource._html_template = """
            <html>
                <head>
                    <title>$account_email</title>
                </head>
            </html>"""
        self.web = DummySite(root_resource)

    def test_render_GET_should_template_account_email(self):
        request = DummyRequest([''])

        d = self.web.get(request)

        def assert_response(_):
            expected = """
            <html>
                <head>
                    <title>hackerman@pixelated.org</title>
                </head>
            </html>"""

            actual = request.written[0]
            self.assertEquals(expected, actual)

        d.addCallback(assert_response)
        return d
