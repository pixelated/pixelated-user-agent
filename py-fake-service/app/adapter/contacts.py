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
import re


class Contacts:

    def __init__(self):
        self.contacts = []

    def add(self, mbox_mail):
        contact = mbox_mail.get('From')
        self.contacts.append(Contact(contact))

    def search(self, query):
        contacts_query = re.compile(query)
        return [
            contact.__dict__
            for contact in self.contacts
            if contacts_query.match(contact.addresses[0])
        ]


class Contact:

    def __init__(self, contact):
        self.addresses = [contact]
        self.name = ''
