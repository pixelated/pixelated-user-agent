#
# Copyright (c) 2015 ThoughtWorks, Inc.
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

from email.parser import Parser


class BodyParser(object):

    def __init__(self, content, content_type='text/plain; charset="us-ascii"', content_transfer_encoding=None):
        self._content = content
        self._content_type = content_type
        self._content_transfer_encoding = content_transfer_encoding

    def parsed_content(self):
        parser = Parser()

        text=''
        text += 'Content-Type: %s\n' % self._content_type
        if self._content_transfer_encoding is not None:
            text += 'Content-Transfer-Encoding: %s\n' % self._content_transfer_encoding
        text += '\n'
        text += self._content

        parsed_body = parser.parsestr(text)

        result = unicode(parsed_body.get_payload(decode=True), encoding='utf-8')

        return unicode(result)