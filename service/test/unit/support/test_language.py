#
# Copyright (c) 2017 ThoughtWorks, Inc.
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


from twisted.trial import unittest

from pixelated.support.language import parse_accept_language


class TestParseAcceptLanguage(unittest.TestCase):
    def test_parse_pt_br_simple(self):
        all_headers = {
            'accept-language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'}
        parsed_language = parse_accept_language(all_headers)
        self.assertEqual('pt-BR', parsed_language)

    def test_parse_en_us_simple(self):
        all_headers = {
            'accept-language': 'en-US,en;q=0.8,en-US;q=0.5,en;q=0.3'}
        parsed_language = parse_accept_language(all_headers)
        self.assertEqual('en-US', parsed_language)

    def test_parse_pt_br_as_default(self):
        all_headers = {
            'accept-language': 'de-DE,de;q=0.8,en-US;q=0.5,en;q=0.3'}
        parsed_language = parse_accept_language(all_headers)
        self.assertEqual('pt-BR', parsed_language)
