import unittest
from mockito import mock
from pixelated.config.site import PixelatedSite
from twisted.protocols.basic import LineReceiver


class TestPixelatedSite(unittest.TestCase):
    def test_add_csp_header_request(self):
        request = self.create_request()
        request.process()
        headers = request.headers
        self.assertEqual(headers.get("Content-Security-Policy"), "default-src 'self'; style-src 'self' 'unsafe-inline'")

    def create_request(self):
        channel = LineReceiver()
        channel.site = PixelatedSite(mock())
        request = PixelatedSite.requestFactory(channel=channel, queued=True)
        request.method = "GET"
        request.uri = "localhost"
        request.clientproto = 'HTTP/1.1'
        request.prepath = []
        request.postpath = request.uri.split('/')[1:]
        request.path = "/"
        return request
