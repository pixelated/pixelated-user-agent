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

from flask import send_file
from flask import request

import io
import re
from twisted.web.server import NOT_DONE_YET


class AttachmentsController:

    def __init__(self, querier):
        self.querier = querier

    def attachment(self, request, attachment_id):
        encoding = request.args.get('encoding', [''])[0]
        attachment = self.querier.attachment(attachment_id, encoding)
        request.setRawHeader('Content-Type', self._extract_mimetype(attachment['content-type']))
        request.write(io.BytesIO(attachment['content']))

        return NOT_DONE_YET

    def _extract_mimetype(self, content_type):
        match = re.compile('([A-Za-z-]+\/[A-Za-z-]+)').search(content_type)
        return match.group(1)
