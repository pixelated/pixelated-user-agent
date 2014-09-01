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
from mock import Mock
from datetime import datetime

LEAP_FLAGS = ['\\Seen',
              '\\Answered',
              '\\Flagged',
              '\\Deleted',
              '\\Draft',
              '\\Recent',
              'List']


def mail_dict():
    return {
        'header': {
            'to': ['to@pixelated.org', 'anotherto@pixelated.org'],
            'cc': ['cc@pixelated.org', 'anothercc@pixelated.org'],
            'bcc': ['bcc@pixelated.org', 'anotherbcc@pixelated.org'],
            'subject': 'Subject'
        },
        'body': 'Body',
        'ident': '',
        'tags': []
    }


def leap_mail(uid=0, leap_flags=LEAP_FLAGS, extra_flags=[], headers={'date': str(datetime.now())}):
    flags = leap_flags + extra_flags
    return Mock(getUID=Mock(return_value=uid),
                getFlags=Mock(return_value=flags),
                bdoc=Mock(content={'raw': 'test'}),
                hdoc=Mock(content={'headers': headers}))


def leap_mailbox(leap_flags=LEAP_FLAGS, extra_flags=[]):
    flags = leap_flags + extra_flags
    return Mock(getFlags=Mock(return_value=flags),
                _get_mbox_doc=Mock(return_value=None),
                messages=[leap_mail(uid=6, leap_flags=[], extra_flags=[])])
