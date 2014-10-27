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

import os
import logging
from flask import Flask
from leap.common.events import server as events_server
from pixelated.config import app_factory
import pixelated.config.args as input_args
import pixelated.bitmask_libraries.register as leap_register
from pixelated.bitmask_libraries.leap_srp import LeapAuthException
import pixelated.config.credentials_prompt as credentials_prompt
import pixelated.config.reactor_manager as reactor_manager
import pixelated.support.ext_protobuf  # monkey patch for protobuf in OSX
import pixelated.support.ext_sqlcipher  # monkey patch for sqlcipher in debian


app = Flask(__name__, static_url_path='', static_folder=app_factory.get_static_folder())


def setup():
    try:
        args = input_args.parse()
        app.config.update({'HOST': args.host, 'PORT': args.port})

        debugger = setup_debugger(args.debug)

        if args.register:
            register(*args.register[::-1])
        else:
            if args.dispatcher:
                raise Exception('Dispatcher mode not implemented yet')
            else:
                configuration_setup(app, args.config)
            start_services(app, debugger)
    finally:
        reactor_manager.stop_reactor_on_exit()


def register(username, server_name):
    try:
        leap_register.register_new_user(username, server_name)
    except LeapAuthException:
        print('User already exists')

def setup_debugger(enabled):
    debug_enabled = enabled or os.environ.get('DEBUG', False)
    if not debug_enabled:
        logging.basicConfig()
        logger = logging.getLogger('werkzeug')
        logger.setLevel(logging.INFO)

def configuration_setup(app, config):
    if config is not None:
        config_file = os.path.abspath(os.path.expanduser(config))
        app.config.from_pyfile(config_file)
    else:
        provider, user, password = credentials_prompt.run()
        app.config['LEAP_SERVER_NAME'] = provider
        app.config['LEAP_USERNAME'] = user
        app.config['LEAP_PASSWORD'] = password

def start_services(app, debug):
    reactor_manager.start_reactor(logging=debug)
    events_server.ensure_server(port=8090)
    app_factory.create_app(app, debug)


if __name__ == '__main__':
    setup()
