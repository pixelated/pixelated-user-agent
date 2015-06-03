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

import json
import sys
import os


def config_dispatcher(dispatcher):

    def fetch_credentials_from_dispatcher(filename):
        if not os.path.exists(filename):
            print('The credentials pipe doesn\'t exist')
            sys.exit(1)
        with open(filename, 'r') as fifo:
            return json.loads(fifo.read())

    def fetch_credentials_from_dispatcher_stdin():
        return json.loads(sys.stdin.read())

    config = fetch_credentials_from_dispatcher(dispatcher) if dispatcher else fetch_credentials_from_dispatcher_stdin()

    return (config['leap_provider_hostname'],
            config['user'],
            config['password'])
