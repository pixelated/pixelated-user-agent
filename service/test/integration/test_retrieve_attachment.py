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
import base64
import json
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from poster.encode import multipart_encode, MultipartParam
from twisted.internet import defer

from test.support.integration.soledad_test_base import SoledadTestBase


class RetrieveAttachmentTest(SoledadTestBase):

    @defer.inlineCallbacks
    def test_attachment_content_is_retrieved(self):
        attachment_id, input_mail = self._create_mail_with_attachment()
        yield self.mail_store.add_mail('INBOX', input_mail.as_string())

        attachment, req = yield self.get_attachment(attachment_id, 'base64')

        self.assertEqual(200, req.code)
        self.assertEquals('pretend to be binary attachment data', attachment)

    def _create_mail_with_attachment(self):
        input_mail = MIMEMultipart()
        input_mail.attach(MIMEText(u'a utf8 message', _charset='utf-8'))
        attachment = MIMEApplication('pretend to be binary attachment data')
        attachment.add_header('Content-Disposition', 'attachment', filename='filename.txt')
        input_mail.attach(attachment)
        attachment_id = 'B5B4ED80AC3B894523D72E375DACAA2FC6606C18EDF680FE95903086C8B5E14A'
        return attachment_id, input_mail

    @defer.inlineCallbacks
    def test_attachment_error_returned_if_id_not_found(self):
        attachment, req = yield self.get_attachment('invalid attachment id', 'base64')

        self.assertEqual(404, req.code)
        self.assertIsNone(attachment)

    @defer.inlineCallbacks
    def test_post_new_attachment(self):
        content_type = 'text/plain'
        filename = 'filename.txt'
        data = 'pretend to be binary attachment data'
        file = MultipartParam('attachment', value=data, filename=filename, filetype=content_type)
        datagen, headers = multipart_encode([file])
        post_data = "".join(datagen)

        _, req = yield self.post_attachment(post_data, headers)

        self.assertEqual(201, req.code)
        self.assertEqual('/attachment/B5B4ED80AC3B894523D72E375DACAA2FC6606C18EDF680FE95903086C8B5E14A', req.headers['Location'])
        response_json = {'attachment_id': 'B5B4ED80AC3B894523D72E375DACAA2FC6606C18EDF680FE95903086C8B5E14A',
                         'content-type': content_type,
                         'filename': filename,
                         'filesize': len(data)}
        self.assertEqual(response_json, json.loads(req.written[0]))
