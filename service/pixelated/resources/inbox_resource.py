#
# Copyright (c) 2016 ThoughtWorks, Inc.
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
import hashlib
import os
from string import Template

import pixelated
from pixelated.resources import BaseResource

from twisted.logger import Logger

logger = Logger()


MODE_STARTUP = 1
MODE_RUNNING = 2


class InboxResource(BaseResource):
    isLeaf = True

    def __init__(self, services_factory):
        BaseResource.__init__(self, services_factory)
        self._templates_folder = self._get_templates_folder()
        self._html_template = open(os.path.join(self._templates_folder, 'index.html')).read()
        with open(os.path.join(self._templates_folder, 'Interstitial.html')) as f:
            self.interstitial = f.read()
        self._mode = MODE_STARTUP

    def initialize(self):
        self._mode = MODE_RUNNING
        logger.debug('Inbox in RUNNING mode. %s' % self)

    def _get_templates_folder(self):
        path = os.path.dirname(os.path.abspath(pixelated.__file__))
        return os.path.join(path, 'assets')

    def _is_starting(self):
        return self._mode == MODE_STARTUP

    def render_GET(self, request):
        logger.debug('Inbox rendering GET. %s' % self)
        self._add_csrf_cookie(request)
        if self._is_starting():
            logger.debug('Inbox rendering interstitial. %s' % self)
            return self.interstitial
        else:
            logger.debug('Inbox rendering from template. %s' % self)
            account_email = self.mail_service(request).account_email
            response = Template(self._html_template).safe_substitute(account_email=account_email)
            return str(response)
