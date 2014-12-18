#
# Copyright (c) 2014 ThoughtWorks Deutschland GmbH
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
import traceback
import sys

from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado import gen


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        self.forward('3333', '127.0.0.1')

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        self.get()

    @tornado.web.asynchronous
    @gen.engine
    def put(self):
        self.get()

    @tornado.web.asynchronous
    @gen.engine
    def delete(self):
        self.get()

    def handle_response(self, response):
        if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
            print(self.request.uri)
            print(response.error)
            self.set_status(500)
            self.write("Internal server error:\n" + str(response.error))
            self.finish()
        else:
            self.set_status(response.code)
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            if response.body:
                self.write(response.body)
            self.finish()

    def forward(self, port=None, host=None):
        url = "%s://%s:%s%s" % (
            'http', host or "127.0.0.1", port or 80, self.request.uri)
        try:
            tornado.httpclient.AsyncHTTPClient().fetch(
                tornado.httpclient.HTTPRequest(
                    url=url,
                    method=self.request.method,
                    body=None if not self.request.body else self.request.body,
                    headers=self.request.headers,
                    follow_redirects=False,
                    request_timeout=10),
                self.handle_response)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, 'response') and x.response:
                self.handle_response(x.response)
        except Exception, e:
            self.set_status(500)
            self.write("Internal server error:\n" + ''.join(traceback.format_exception(*sys.exc_info())))
            self.finish()


def _create_app():
    app = tornado.web.Application(
        [
            (r"/.*", MainHandler)
        ],
        xsrf_cookies=False,
        debug=True)
    return app


class Proxy:

    def __init__(self):
        pass

    def serve_forever(self):
        app = _create_app()
        self._server = HTTPServer(app)
        self._server.listen(port='8888', address='127.0.0.1')
        self._ioloop = tornado.ioloop.IOLoop.instance()
        self._ioloop.start()  # this is a blocking call, server has stopped on next line
        self._ioloop = None

    def shutdown(self):
        if self._ioloop:
            self._server.stop()
            self._ioloop.stop()


proxy = Proxy()
try:
    proxy.serve_forever()
except Exception:
    proxy.shutdown()
