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
import sys, os
sys.path.insert(0, os.environ['APP_ROOT'])

from search import SearchQuery

def test_one_tag():
    assert SearchQuery.compile(u"in:inbox")["tags"] == ["inbox"]
    assert SearchQuery.compile(u"in:trash")["tags"] == ["trash"]
    

def test_two_tags_or():
    assert SearchQuery.compile(u"in:inbox or in:trash")["tags"] == ["inbox", "trash"]

    
def test_tag_negate():
    assert SearchQuery.compile(u"-in:trash")["not_tags"] == ["trash"]

def test_general_search():
    assert SearchQuery.compile(u"searching")["general"] == "searching"

def test_tags_with_quotes():
    assert SearchQuery.compile(u"in:\"inbox\"")["tags"] == ["inbox"]
