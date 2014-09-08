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

DEFAULT_HEADERS = {'date': str(datetime.now())}


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


def leap_mail(uid=0, flags=LEAP_FLAGS, headers=DEFAULT_HEADERS, extra_headers={}):
    headers = dict(headers.items() + extra_headers.items())
    return Mock(getUID=Mock(return_value=uid),
                getFlags=Mock(return_value=flags),
                bdoc=Mock(content={'raw': 'test'}),
                hdoc=Mock(content={'headers': headers}))


def leap_mailbox(messages=[leap_mail(uid=6)], mailbox_name='INBOX'):
    return Mock(_get_mbox_doc=Mock(return_value=None),
                mbox=mailbox_name,
                messages=messages)
