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

import argparse

import os


def parse():
    default_config_path = os.path.join(os.environ['HOME'], '.pixelated')
    parser = argparse.ArgumentParser(description='Pixelated user agent.')
    parser.add_argument('--debug', action='store_true',
                        help='DEBUG mode.')
    parser.add_argument('--register', metavar='username', help='register user with name.')
    parser.add_argument('-c', '--config', metavar='configfile', default=default_config_path,
                        help='use specified config file. Default is ~/.pixelated.')
    args = parser.parse_args()
    return args
