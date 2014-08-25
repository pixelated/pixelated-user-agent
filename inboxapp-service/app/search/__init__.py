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
from scanner import StringScanner, StringRegexp


def _next_token():
    return StringRegexp('[^\s]+')


def _separators():
    return StringRegexp('[\s&]+')


def _compile_tag(compiled, token):
    tag = token.split(":").pop()
    if token[0] == "-":
        compiled["not_tags"].append(tag)
    else:
        compiled["tags"].append(tag)
    return compiled


class SearchQuery:

    @staticmethod
    def compile(query):
        compiled = {"tags": [], "not_tags": []}

        scanner = StringScanner(query.encode('utf8').replace("\"", ""))
        first_token = True
        while not scanner.is_eos:
            token = scanner.scan(_next_token())

            if not token:
                scanner.skip(_separators())
                continue

            if ":" in token:
                compiled = _compile_tag(compiled, token)
            elif first_token:
                compiled["general"] = token

            if not first_token:
                first_token = True

        return compiled
