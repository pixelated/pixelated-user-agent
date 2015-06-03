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
from pixelated.bitmask_libraries.config import DEFAULT_LEAP_HOME


def parse_user_agent_args():
    parser = argparse.ArgumentParser(description='Pixelated user agent.')

    parser_add_default_arguments(parser)

    parser.add_argument('--host', default='127.0.0.1', help='the host to run the user agent on')
    parser.add_argument('--port', type=int, default=3333, help='the port to run the user agent on')
    parser.add_argument('-sk', '--sslkey', metavar='<server.key>', default=None, help='use specified file as web server\'s SSL key (when using the user-agent together with the pixelated-dispatcher)')
    parser.add_argument('-sc', '--sslcert', metavar='<server.crt>', default=None, help='use specified file as web server\'s SSL certificate (when using the user-agent together with the pixelated-dispatcher)')
    parser.add_argument('--register', metavar=('provider', 'username'),
                        nargs=2, help='register a new username on the desired LEAP provider')
    args = parser.parse_args()
    return args


def parse_maintenance_args():
    parser = argparse.ArgumentParser(description='pixelated maintenance')
    parser_add_default_arguments(parser)
    subparsers = parser.add_subparsers(help='commands', dest='command')
    subparsers.add_parser('reset', help='reset account command')
    mails_parser = subparsers.add_parser('load-mails', help='load mails into account')
    mails_parser.add_argument('file', nargs='+', help='file(s) with mail data')

    subparsers.add_parser('dump-soledad', help='dump the soledad database')
    subparsers.add_parser('sync', help='sync the soledad database')

    return parser.parse_args()


def parser_add_default_arguments(parser):
    parser.add_argument('--debug', action='store_true', help='DEBUG mode.')
    parser.add_argument('--dispatcher', help='run in organization mode, the credentials will be read from specified file', metavar='file')
    parser.add_argument('--dispatcher-stdin', help='run in organization mode, the credentials will be read from stdin', default=False, action='store_true', dest='dispatcher_stdin')
    parser.add_argument('-c', '--config', metavar='<configfile>', default=None, help='use specified file for credentials (for test purposes only)')
    parser.add_argument('--home', help='The folder where the user agent stores its data. Defaults to ~/.leap', default=DEFAULT_LEAP_HOME)
    parser.add_argument('-lc', '--leap-provider-cert', metavar='<leap-provider.crt>', default=None, help='use specified file for LEAP provider cert authority certificate (url https://<LEAP-provider-domain>/ca.crt)')
    parser.add_argument('-lf', '--leap-provider-cert-fingerprint', metavar='<leap provider certificate fingerprint>', default=None, help='use specified fingerprint to validate connection with LEAP provider', dest='leap_provider_cert_fingerprint')
