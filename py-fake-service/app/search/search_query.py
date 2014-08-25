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
import re


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
        compiled = {"tags": [], "not_tags": [], "general": []}

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
                compiled["general"].append(token)

            if not first_token:
                first_token = True

        compiled["general"] = ' '.join(compiled["general"])
        return SearchQuery(compiled)

    def __init__(self, compiled):
        self.compiled = compiled

    def test(self, mail):
        if 'all' in self.compiled.get('tags'):
            return True

        if set(self.compiled.get('not_tags')).intersection(set(mail.tags)):
            return False

        if set(self.compiled.get('tags')).intersection(set(mail.tags)):
            return True

        if self.compiled.get('general'):
            search_terms = re.compile(
                self.compiled['general'],
                flags=re.IGNORECASE)
            if search_terms.search(mail.subject+' '+mail.body):
                return True

        if not [v for v in self.compiled.values() if v]:
            return True

        return False
