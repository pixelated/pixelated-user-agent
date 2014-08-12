class Tag:
    DEFAULT_TAGS = ["inbox", "sent", "trash", "drafts"] 

    def __init__(self, name, ident):
        self.counts = {
            'total': 1,
            'read': 0,
            'starred': 0,
            'reply': 0
        }   

        self.ident = ident
        self.name = name
        self.default = name in self.DEFAULT_TAGS

    def increment_count(self):
        self.counts['total'] += 1
