#
# Copyright (c) 2014 ThoughtWorks, Inc.
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
import cgi
import io
import re

from twisted.internet import defer
from twisted.protocols.basic import FileSender
from twisted.python.log import msg
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

from pixelated.resources import respond_json_deferred


class AttachmentResource(Resource):
    isLeaf = True

    def __init__(self, mail_service, attachment_id):
        Resource.__init__(self)
        self.attachment_id = attachment_id
        self.mail_service = mail_service

    def render_GET(self, request):
        def error_handler(failure):
            msg(failure, 'attachment not found')
            request.code = 404
            request.finish()

        encoding = request.args.get('encoding', [None])[0]
        filename = request.args.get('filename', [self.attachment_id])[0]
        request.setHeader(b'Content-Type', b'application/force-download')
        request.setHeader(b'Content-Disposition', bytes('attachment; filename=' + filename))

        d = self._send_attachment(encoding, filename, request)
        d.addErrback(error_handler)

        return server.NOT_DONE_YET

    @defer.inlineCallbacks
    def _send_attachment(self, encoding, filename, request):
        attachment = yield self.mail_service.attachment(self.attachment_id)

        bytes_io = io.BytesIO(attachment['content'])

        try:
            request.code = 200
            yield FileSender().beginFileTransfer(bytes_io, request)
        finally:
            bytes_io.close()
            request.finish()

    def _extract_mimetype(self, content_type):
        match = re.compile('([A-Za-z-]+\/[A-Za-z-]+)').search(content_type)
        return match.group(1)


class AttachmentsResource(Resource):
    BASE_URL = 'attachment'

    def __init__(self, mail_service):
        Resource.__init__(self)
        self.mail_service = mail_service

    def getChild(self, attachment_id, request):
        return AttachmentResource(self.mail_service, attachment_id)

    def render_GET(self, request):
        return '<html><body><p></p>' \
               '<form method="POST" enctype="multipart/form-data">' \
               '<input name="attachment" type="file" /> <p></p>' \
               '<input type="submit" /></form><p></p>' \
               '</body></html>'

    def render_POST(self, request):
        fields = cgi.FieldStorage(fp=request.content, headers=request.headers, environ={'REQUEST_METHOD':'POST'})
        _file = fields['attachment']
        deferred = defer.maybeDeferred(self.mail_service.attachment_id, _file.value, _file.type)

        def send_location(attachment_id):
            request.headers['Location'] = '/%s/%s'% (self.BASE_URL, attachment_id)
            respond_json_deferred({"attachment_id": attachment_id}, request, status_code=201)

        def error_handler(error):
            print error
            respond_json_deferred({"message": "Something went wrong. Attachement not saved."}, request, status_code=500)

        deferred.addCallback(send_location)
        deferred.addErrback(error_handler)

        return NOT_DONE_YET
