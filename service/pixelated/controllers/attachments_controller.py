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

import io
import re
from twisted.protocols.basic import FileSender
from twisted.python.log import err


class AttachmentsController:

    def __init__(self, querier):
        self.querier = querier

    def attachment(self, request, attachment_id):
        encoding = request.args.get('encoding', [None])[0]
        filename = request.args.get('filename', [attachment_id])[0]
        attachment = self.querier.attachment(attachment_id, encoding)

        request.setHeader(b'Content-Type', b'application/force-download')
        request.setHeader(b'Content-Disposition', bytes('attachment; filename=' + filename))
        bytes_io = io.BytesIO(attachment['content'])
        d = FileSender().beginFileTransfer(bytes_io, request)

        def cbFinished(ignored):
            bytes_io.close()
            request.finish()

        d.addErrback(err).addCallback(cbFinished)

        return d

    def _extract_mimetype(self, content_type):
        match = re.compile('([A-Za-z-]+\/[A-Za-z-]+)').search(content_type)
        return match.group(1)
