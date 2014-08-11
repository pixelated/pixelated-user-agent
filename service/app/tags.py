class Tag:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()


class Tags:

    SPECIAL_TAGS = ['inbox', 'sent', 'drafts', 'trash']

    def __init__(self):
        self.tags = set([Tag(name) for name in self.SPECIAL_TAGS])

    def add(self, name):
        self.tags.add(Tag(name))

    def find(self, name):
        for tag in self.tags:
            if tag.name == name:
                return tag

    def __len__(self):
        return len(self.tags)

    def __iter__(self):
        return self.tags.__iter__()