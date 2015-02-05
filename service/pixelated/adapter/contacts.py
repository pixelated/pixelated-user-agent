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
from email.utils import parseaddr


def address_duplication_filter(contacts):
    contacts_by_mail = dict()

    for contact in contacts:
        mail_address = extract_mail_address(contact)
        previous = contacts_by_mail.get(mail_address, '')
        contacts_by_mail[mail_address] = contact if len(contact) > len(previous) else previous
    return contacts_by_mail.values()


def extract_mail_address(text):
    return parseaddr(text)[1]
