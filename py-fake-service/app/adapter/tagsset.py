from tag import Tag

class TagsSet:
    def __init__(self):
        self.tags = {}
        self.ident = 0

    def add(self, mbox_mail):
        tags = mbox_mail.get('X-TW-Pixelated-Tags').split(', ')
        for tag in tags:
            tag = self._create_new_tag(tag)
            tag.increment_count()
            
    def all_tags(self):
        return self.tags.values()

    def mark_as_read(self, tags):
        for tag in tags:
            tag = tag.lower()
            tag = self.tags.get(tag)
            tag.increment_read()

    def increment_tag_total_count(self, tagname):
        tag = self.tags.get(tagname)
        if tag:
            tag.increment_count()
        else:
            self._create_new_tag(tagname)
        
    def decrement_tag_total_count(self, tag):
        self.tags.get(tag).decrement_count()

    def _create_new_tag(self, tag):
        tag = Tag(tag, self.ident)
        tag = self.tags.setdefault(tag.name, tag)
        self.ident += 1
        return tag


