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
import datetime
import dateutil.parser

from dateutil.tz import tzlocal


def iso_now():
    return datetime.datetime.now(tzlocal()).isoformat()


def milliseconds(date):
    date = dateutil.parser.parse(date)
    date = date.replace(tzinfo=None)
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = date - epoch
    return int(delta.total_seconds() * 1000)
