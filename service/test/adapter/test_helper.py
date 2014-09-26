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
from pixelated.adapter.pixelated_mail import InputMail

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


def doc(content):
    class TestDoc:
        def __init__(self, content):
            self.content = content

    return TestDoc(content)


def leap_mail(uid=0, flags=LEAP_FLAGS, headers=DEFAULT_HEADERS, extra_headers={}, mbox='INBOX', body='body',
              chash='chash'):
    fdoc = doc({'flags': flags, 'mbox': mbox, 'type': 'flags', 'uid': uid, 'chash': chash})

    headers['headers'] = extra_headers
    hdoc = doc(headers)

    bdoc = doc({'raw': body, 'type': 'cnt'})

    return (fdoc, hdoc, bdoc)


def input_mail():
    mail = InputMail()
    mail.fdoc = doc({})
    mail._chash = "123"
    mail.as_dict = lambda: None
    return mail

