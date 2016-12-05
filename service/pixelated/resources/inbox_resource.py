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
import pkg_resources
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
        with open(pkg_resources.resource_filename('templates', 'index.html')) as f:
            self._html_template = f.read()
        with open(pkg_resources.resource_filename('templates', 'Interstitial.html')) as f:
            self.interstitial = f.read()
        self._mode = MODE_STARTUP

    def initialize(self):
        self._mode = MODE_RUNNING

    def _is_starting(self):
        return self._mode == MODE_STARTUP

    def render_GET(self, request):
        if self._is_starting():
            return self.interstitial
        else:
            account_email = self.mail_service(request).account_email
            response = Template(self._html_template).safe_substitute(account_email=account_email)
            return str(response)
