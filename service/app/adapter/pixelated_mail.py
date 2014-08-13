from app.tags import Tag


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
        self.headers = self.extract_headers(leap_mail)
        self.ident = leap_mail.getUID()
        self.status = self.extract_status(leap_mail)
        self.security_casing = {}
        self.tags = self.extract_tags(leap_mail)

    def extract_status(self, leap_mail):
        flags = leap_mail.getFlags()
        return [converted for flag, converted in self.LEAP_FLAGS_STATUSES.items() if flag in flags]

    def extract_headers(self, leap_mail):
        temporary_headers = {}
        for header, value in leap_mail.hdoc.content['headers'].items():
            temporary_headers[header.lower()] = value
        return temporary_headers

    def extract_tags(self, leap_mail):
        flags = leap_mail.getFlags()
        converted_tags = [Tag(converted) for flag, converted in self.LEAP_FLAGS_TAGS.items() if flag in flags]
        tags = converted_tags + [Tag(flag) for flag in leap_mail.getFlags() if flag not in self.LEAP_FLAGS]
        return tags

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
