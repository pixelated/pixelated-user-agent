from app.tags import Tag
from app.tags import Tags


class PixelatedMail:

    LEAP_FLAGS = ['\\Seen',
                  '\\Answered',
                  '\\Flagged',
                  '\\Deleted',
                  '\\Draft',
                  '\\Recent',
                  'List']

    LEAP_FLAGS_STATUSES = {
        '\\Seen': 'read',
        '\\Answered': 'replied'
    }

    LEAP_FLAGS_TAGS = {
        '\\Deleted': 'trash',
        '\\Draft': 'drafts',
        '\\Recent': 'inbox'
    }

    def __init__(self, leap_mail):
        self.leap_mail = leap_mail
        self.body = leap_mail.bdoc.content['raw']
        self.headers = self.extract_headers()
        self.ident = leap_mail.getUID()
        self.status = self.extract_status()
        self.security_casing = {}
        self.tags = self.extract_tags()

    def extract_status(self):
        flags = self.leap_mail.getFlags()
        return [converted for flag, converted in self.LEAP_FLAGS_STATUSES.items() if flag in flags]

    def extract_headers(self):
        temporary_headers = {}
        for header, value in self.leap_mail.hdoc.content['headers'].items():
            temporary_headers[header.lower()] = value
        return temporary_headers

    def extract_tags(self):
        flags = self.leap_mail.getFlags()
        tag_names = self._converted_tags(flags) + self._custom_tags(flags)
        tags = []
        for tag in tag_names:
            tags.append(Tag(tag))
        return tags

    def _converted_tags(self, flags):
        return [converted for flag, converted in self.LEAP_FLAGS_TAGS.items() if flag in flags]

    def _custom_tags(self, flags):
        return [self._remove_prefix(flag) for flag in self.leap_mail.getFlags() if flag.startswith('tag_')]

    def _remove_prefix(self, flag_name):
        return flag_name.replace('tag_', '', 1)

    def update_tags(self, tags):
        self.tags = [Tag(tag) for tag in tags]
        return self.tags

    def has_tag(self, tag):
        return Tag(tag) in self.tags

    def as_dict(self):
        tags = [tag.name for tag in self.tags]
        return {
            'header': self.headers,
            'ident': self.ident,
            'tags': tags,
            'status': self.status,
            'security_casing': self.security_casing,
            'body': self.body
        }
