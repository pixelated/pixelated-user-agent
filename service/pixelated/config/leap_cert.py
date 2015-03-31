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

import pixelated.bitmask_libraries.certs as certs


def init_leap_cert(args):
    if args.leap_cert_fingerprint is None:
        certs.LEAP_CERT = args.leap_cert
        certs.LEAP_FINGERPRINT = None
    else:
        certs.LEAP_FINGERPRINT = args.leap_cert_fingerprint
        certs.LEAP_CERT = False
