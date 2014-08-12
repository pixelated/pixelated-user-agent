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
