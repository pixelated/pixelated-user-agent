import sys, os
sys.path.insert(0, os.environ['APP_ROOT'])

from app.search import SearchQuery

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
