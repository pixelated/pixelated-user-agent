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
import inboxapp

class ProviderNotFoundException(Exception):
    def __init__(self, provider):
        self.provider = provider

    def __str__(self):
        return "Provider '%s' not found" % self.provider

class ClientFactory:

    @staticmethod
    def create(provider, account):
        if provider  == 'inboxapp':
            return inboxapp.Client(account)
        raise ProviderNotFoundException(provider)

class MailConverterFactory:

    @staticmethod
    def create(provider, client):
        if provider ==  'inboxapp':
            return inboxapp.MailConverter(client)
        raise ProviderNotFoundException(provider)

