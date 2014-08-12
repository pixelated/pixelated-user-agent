from tag import Tag

class TagsSet:
    def __init__(self):
        self.tags = {}
        self.ident = 0

    def add(self, mbox_mail):
        tags = mbox_mail.get('X-TW-Pixelated-Tags').split(', ')
        for tag in tags:
            tag = self.tags.setdefault(tag, Tag(tag, self.ident))
            tag.increment_count()
            self.ident += 1 
            
    def all_tags(self):
        return self.tags.values()

    def mark_as_read(self, tags):
        for tag in tags:
            tag = self.tags.get(tag)
            tag.increment_read()

    def increment_tag_total_count(self, tag):
        self.tags.get(tag).increment_count()
        
    def decrement_tag_total_count(self, tag):
        self.tags.get(tag).decrement_count()

