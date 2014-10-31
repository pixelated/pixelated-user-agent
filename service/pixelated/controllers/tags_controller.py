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

from flask import request
from pixelated.controllers import respond_json


class TagsController:

    def __init__(self, search_engine):
        self._search_engine = search_engine

    def tags(self, request):
        query = request.args.get('q', [''])[0]
        skip_default_tags = request.args.get('skipDefaultTags')
        tags = self._search_engine.tags(query=query, skip_default_tags=skip_default_tags)
        return respond_json(tags, request)
