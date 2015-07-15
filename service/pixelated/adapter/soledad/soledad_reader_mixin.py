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
import logging
import quopri
import re

from twisted.internet import defer
from pixelated.adapter.model.mail import PixelatedMail
from pixelated.adapter.soledad.soledad_facade_mixin import SoledadDbFacadeMixin


logger = logging.getLogger(__name__)


class SoledadReaderMixin(SoledadDbFacadeMixin, object):

    @defer.inlineCallbacks
    def all_mails(self):
        fdocs_chash = [(fdoc, fdoc.content['chash']) for fdoc in (yield self.get_all_flags())]
        if len(fdocs_chash) == 0:
            defer.returnValue([])
        defer.returnValue((yield self._build_mails_from_fdocs(fdocs_chash)))

    @defer.inlineCallbacks
    def _build_mails_from_fdocs(self, fdocs_chash):
        if len(fdocs_chash) == 0:
            defer.returnValue([])

        fdocs_hdocs = []
        for fdoc, chash in fdocs_chash:
            hdoc = yield self.get_header_by_chash(chash)
            if not hdoc:
                continue
            fdocs_hdocs.append((fdoc, hdoc))

        fdocs_hdocs_bodyphash = [(f[0], f[1], f[1].content.get('body')) for f in fdocs_hdocs]
        fdocs_hdocs_bdocs_parts = []
        for fdoc, hdoc, body_phash in fdocs_hdocs_bodyphash:
            bdoc = yield self.get_content_by_phash(body_phash)
            if not bdoc:
                continue
            parts = yield self._extract_parts(hdoc.content)
            fdocs_hdocs_bdocs_parts.append((fdoc, hdoc, bdoc, parts))

        defer.returnValue([PixelatedMail.from_soledad(*raw_mail, soledad_querier=self) for raw_mail in fdocs_hdocs_bdocs_parts])

    def mail_exists(self, ident):
        return self.get_flags_by_chash(ident)

    @defer.inlineCallbacks
    def mail(self, ident):
        fdoc = yield self.get_flags_by_chash(ident)
        hdoc = yield self.get_header_by_chash(ident)
        bdoc = yield self.get_content_by_phash(hdoc.content['body'])
        parts = yield self._extract_parts(hdoc.content)

        mail = PixelatedMail.from_soledad(fdoc, hdoc, bdoc, parts=parts, soledad_querier=self)
        defer.returnValue(mail)

    @defer.inlineCallbacks
    def mails(self, idents):
        fdocs_chash = [((yield self.get_flags_by_chash(ident)), ident) for ident in
                       idents]
        fdocs_chash = [(result, ident) for result, ident in fdocs_chash if result]
        defer.returnValue((yield self._build_mails_from_fdocs(fdocs_chash)))

    @defer.inlineCallbacks
    def attachment(self, attachment_ident, encoding):
        bdoc = yield self.get_content_by_phash(attachment_ident)
        defer.returnValue({'content': self._try_decode(bdoc.content['raw'], encoding),
                           'content-type': bdoc.content['content-type']})

    def _try_decode(self, raw, encoding):
        encoding = encoding.lower()
        if encoding == 'base64':
            return base64.decodestring(raw)
        elif encoding == 'quoted-printable':
            return quopri.decodestring(raw)
        else:
            return str(raw)

    @defer.inlineCallbacks
    def _extract_parts(self, hdoc, parts=None):
        if not parts:
            parts = {'alternatives': [], 'attachments': []}

        if hdoc['multi']:
            for part_key in hdoc.get('part_map', {}).keys():
                yield self._extract_parts(hdoc['part_map'][part_key], parts)
        else:
            headers_dict = {elem[0]: elem[1] for elem in hdoc.get('headers', [])}
            if 'attachment' in headers_dict.get('Content-Disposition', ''):
                parts['attachments'].append(self._extract_attachment(hdoc, headers_dict))
            else:
                parts['alternatives'].append((yield self._extract_alternative(hdoc, headers_dict)))
        defer.returnValue(parts)

    @defer.inlineCallbacks
    def _extract_alternative(self, hdoc, headers_dict):
        bdoc = yield self.get_content_by_phash(hdoc['phash'])

        if bdoc is None:
            logger.warning("No BDOC content found for message!!!")
            raw_content = ""
        else:
            raw_content = bdoc.content['raw']

        defer.returnValue({'headers': headers_dict, 'content': raw_content})

    def _extract_attachment(self, hdoc, headers_dict):
        content_disposition = headers_dict['Content-Disposition']
        match = re.compile('.*name=\"(.*)\".*').search(content_disposition)
        filename = ''
        if match:
            filename = match.group(1)
        return {'headers': headers_dict, 'ident': hdoc['phash'], 'name': filename}
