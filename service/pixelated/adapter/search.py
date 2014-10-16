import os
import whoosh.index
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import sorting


class SearchEngine(object):
    __slots__ = '_index'

    INDEX_FOLDER = os.path.join(os.environ['HOME'], '.leap', 'search_index')
    DEFAULT_TAGS = ['inbox', 'sent', 'drafts', 'trash']

    def __init__(self):
        if not os.path.exists(self.INDEX_FOLDER):
            os.makedirs(self.INDEX_FOLDER)
        self._index = self._create_index()

    def _add_to_tags(self, tags, seen, skip_default_tags, count_type):
        for tag, count in seen.iteritems():
            if skip_default_tags and tag in self.DEFAULT_TAGS:
                continue
            if not tags.get(tag):
                tags[tag] = {'ident': tag, 'name': tag, 'default': False, 'counts': {'total': 0, 'read': 0}, 'mails': []}
            tags[tag]['counts'][count_type] += count

    def _search_tag_groups(self, query):
        seen = None
        query_string = (query + '*' if query else '*').lower()
        query_parser = QueryParser('tag', self._index.schema)
        options = {'limit': None, 'groupedby': sorting.FieldFacet('tag', allow_overlap=True), 'maptype': sorting.Count}

        with self._index.searcher() as searcher:
            total = searcher.search(query_parser.parse(query_string), **options).groups()
            if not query:
                seen = searcher.search(query_parser.parse('* AND flags:\\Seen'), **options).groups()

        return seen, total

    def _init_tags_defaults(self):
        tags = {}
        for default_tag in self.DEFAULT_TAGS:
            tags[default_tag] = {
                'ident': default_tag,
                'name': default_tag,
                'default': True,
                'counts': {
                    'total': 0,
                    'read': 0
                },
                'mails': []
            }
        return tags

    def _build_tags(self, seen, total, skip_default_tags):
        tags = {}
        if not skip_default_tags:
            tags = self._init_tags_defaults()
        self._add_to_tags(tags, total, skip_default_tags, count_type='total')
        if seen:
            self._add_to_tags(tags, seen, skip_default_tags, count_type='read')
        return tags.values()

    def tags(self, query, skip_default_tags):
        seen, total = self._search_tag_groups(query)
        return self._build_tags(seen, total, skip_default_tags)

    def _mail_schema(self):
        return Schema(
            ident=ID(stored=True, unique=True),
            sender=ID(stored=False),
            to=ID(stored=False),
            cc=ID(stored=False),
            bcc=ID(stored=False),
            subject=TEXT(stored=False),
            body=TEXT(stored=False),
            tag=KEYWORD(stored=False, commas=True),
            flags=KEYWORD(stored=False, commas=True),
            raw=TEXT(stored=False))

    def _create_index(self):
        return whoosh.index.create_in(self.INDEX_FOLDER, self._mail_schema(), indexname='mails')

    def index_mail(self, mail):
        with self._index.writer() as writer:
            self._index_mail(writer, mail)

    def _index_mail(self, writer, mail):
        mdict = mail.as_dict()
        header = mdict['header']
        tags = mdict.get('tags', [])
        tags.append(mail.mailbox_name.lower())
        index_data = {
            'sender': unicode(header.get('from', '')),
            'subject': unicode(header.get('subject', '')),
            'to': unicode(header.get('to', '')),
            'cc': unicode(header.get('cc', '')),
            'bcc': unicode(header.get('bcc', '')),
            'tag': u','.join(tags),
            'body': unicode(mdict['body']),
            'ident': unicode(mdict['ident']),
            'flags': unicode(','.join(mail.flags)),
            'raw': unicode(mail.raw)
        }

        writer.update_document(**index_data)

    def index_mails(self, mails):
        with self._index.writer() as writer:
            for mail in mails:
                self._index_mail(writer, mail)

    def _search_with_options(self, options, query):
        with self._index.searcher() as searcher:
            query = QueryParser('raw', self._index.schema).parse(query)
            results = searcher.search(query, **options)
        return results

    def search(self, query, window, page):
        page = int(page) if (page is not None and int(page) > 0) else 1
        window = int(window) or 25

        query = query.replace('\"', '')
        query = query.replace('-in:', 'AND NOT tag:')
        query = query.replace('in:all', '*')

        with self._index.searcher() as searcher:
            query = QueryParser('raw', self._index.schema).parse(query)
            results = searcher.search_page(query, page, pagelen=window)
            return [mail['ident'] for mail in results]

    def remove_from_index(self, mail_id):
        writer = self._index.writer()
        try:
            writer.delete_by_term('ident', mail_id)
        finally:
            writer.commit()
