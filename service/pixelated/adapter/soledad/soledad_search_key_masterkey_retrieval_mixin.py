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
from pixelated.adapter.soledad.soledad_facade_mixin import SoledadDbFacadeMixin
from cryptography.fernet import Fernet


class SoledadSearchIndexMasterkeyRetrievalMixin(SoledadDbFacadeMixin, object):

    def get_index_masterkey(self):
        index_key = self.get_search_index_masterkey()
        if len(index_key) == 0:
            index_key = Fernet.generate_key()
            self.create_doc(dict(type='index_key', value=index_key))
            return index_key
        return str(index_key[0].content['value'])
