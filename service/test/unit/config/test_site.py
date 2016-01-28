import unittest
from mockito import mock
from pixelated.config.site import PixelatedSite
from twisted.protocols.basic import LineReceiver


class TestPixelatedSite(unittest.TestCase):
    def test_add_csp_header_request(self):
        request = self.create_request()
        request.process()
        headers = request.headers

        header_value = "default-src 'self'; style-src 'self' 'unsafe-inline'"
        self.assertEqual(headers.get("Content-Security-Policy"), header_value)
        self.assertEqual(headers.get("X-Content-Security-Policy"), header_value)
        self.assertEqual(headers.get("X-Webkit-CSP"), header_value)

    def test_add_strict_transport_security_header_if_secure(self):
        request = self.create_request()
        request._forceSSL = True

        request.process()

        headers = request.headers
        self.assertEqual('max-age=31536000; includeSubDomains', headers.get('Strict-Transport-Security'))

    def test_does_not_add_strict_transport_security_header_if_plain_http(self):
        request = self.create_request()

        request.process()

        headers = request.headers
        self.assertFalse('Strict-Transport-Security' in headers)

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
