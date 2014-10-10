import os
import whoosh.index
from whoosh.fields import *
from whoosh.qparser import QueryParser


class SearchEngine(object):
    __slots__ = '_index'

    INDEX_FOLDER = '~/.leap/search_index'

    def __init__(self):
        if not os.path.exists(self.INDEX_FOLDER):
            os.makedirs(self.INDEX_FOLDER)
        self._index = self._create_index()

    def _mail_schema(self):
        return Schema(
            ident=ID(stored=True, unique=True),
            sender=ID(stored=False),
            to=ID(stored=False),
            cc=ID(stored=False),
            bcc=ID(stored=False),
            subject=TEXT(stored=False),
            body=TEXT(stored=False),
            tag=KEYWORD(stored=False, commas=True))

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
            'ident': unicode(mdict['ident'])
        }
        writer.update_document(**index_data)

    def index_mails(self, mails):
        with self._index.writer() as writer:
            for mail in mails:
                self._index_mail(writer, mail)

    def search(self, query):
        query = query.replace('\"', '')
        query = query.replace('-in:', 'AND NOT tag:')
        query = query.replace('in:all', '*')
        with self._index.searcher() as searcher:
            query = QueryParser('body', self._index.schema).parse(query)
            results = searcher.search(query, limit=100)
            return [mail['ident'] for mail in results]

    def remove_from_index(self, mail_id):
        writer = self._index.writer()
        try:
            writer.delete_by_term('ident', mail_id)
        finally:
            writer.commit()
