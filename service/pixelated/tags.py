import json


class Tag:

    def __init__(self, name, default=False):
        self.name = name
        self.default = default
        self.ident = name.__hash__()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()

    def as_dict(self):
        return {
            'name': self.name,
            'default': self.default,
            'ident': self.ident,
            'counts': {
                'total': 0,
                'read': 0,
                'starred': 0,
                'replied': 0
            }
        }


class Tags:

    SPECIAL_TAGS = ['inbox', 'sent', 'drafts', 'trash']

    def __init__(self):
        self.tags = {}
        self.create_default_tags()

    def create_default_tags(self):
        for name in self.SPECIAL_TAGS:
            self.tags[name] = self.add(name)

    def add(self, tag_input):
        if tag_input.__class__.__name__ == 'Tag':
            tag_input = tag_input.name
        tag = Tag(tag_input, tag_input in self.SPECIAL_TAGS)
        self.tags[tag_input] = tag
        return tag

    def find(self, name):
        return self.tags[name]

    def __len__(self):
        return len(self.tags)

    def __iter__(self):
        return self.tags.itervalues()

    def as_dict(self):
        return [tag.as_dict() for tag in self.tags.values()]
