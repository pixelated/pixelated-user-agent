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

import ConfigParser
import os
import getpass


def parse_config_from_file(config_file):
    config_parser = ConfigParser.ConfigParser()
    config_file_path = os.path.abspath(os.path.expanduser(config_file))
    config_parser.read(config_file_path)
    provider, user, password = \
        config_parser.get('pixelated', 'leap_server_name'), \
        config_parser.get('pixelated', 'leap_username'), \
        config_parser.get('pixelated', 'leap_password')

    # TODO: add error messages in case one of the parameters are empty
    return provider, user, password


def prompt_for_credentials():
    provider = raw_input('Which provider do you want to connect to:\n')
    username = raw_input('What\'s your username registered on the provider:\n')
    password = getpass.getpass('Type your password:\n')
    return provider, username, password


def config_user_agent(app, args):
    config_file = args.config
    provider, user, password = parse_config_from_file(config_file) if config_file else prompt_for_credentials()

    app.config['LEAP_SERVER_NAME'] = provider
    app.config['LEAP_USERNAME'] = user
    app.config['LEAP_PASSWORD'] = password
