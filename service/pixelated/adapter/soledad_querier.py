from pixelated.adapter.pixelated_mail import PixelatedMail


class SoledadQuerier:

    instance = None

    def __init__(self, soledad):
        self.soledad = soledad

    @classmethod
    def get_instance(cls, soledad=None):
        if not cls.instance:
            if not soledad:
                raise Exception("Need a soledad for the first time you call this")
            cls.instance = SoledadQuerier(soledad)
        return cls.instance

    def all_mails(self):
        fdocs_chash = [(fdoc, fdoc.content['chash']) for fdoc in self.soledad.get_from_index('by-type', 'flags')]
        if len(fdocs_chash) == 0:
            return []
        return self._build_mails_from_fdocs(fdocs_chash)

    def all_mails_by_mailbox(self, mailbox_name):
        fdocs_chash = [(fdoc, fdoc.content['chash']) for fdoc in self.soledad.get_from_index('by-type-and-mbox', 'flags', mailbox_name)]
        if len(fdocs_chash) == 0:
            return []
        return self._build_mails_from_fdocs(fdocs_chash)

    def _build_mails_from_fdocs(self, fdocs_chash):
        fdocs_hdocs = [(f[0], self.soledad.get_from_index('by-type-and-contenthash', 'head', f[1])[0]) for f in fdocs_chash]
        fdocs_hdocs_phash = [(f[0], f[1], f[1].content.get('body')) for f in fdocs_hdocs]
        fdocs_hdocs_bdocs = [(f[0], f[1], self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', f[2])[0]) for f in fdocs_hdocs_phash]
        return [PixelatedMail.from_soledad(*raw_mail, soledad_querier=self) for raw_mail in fdocs_hdocs_bdocs]

    def save_mail(self, mail):
        # XXX update only what has to be updated
        self.soledad.put_doc(mail.fdoc)
        self.soledad.put_doc(mail.hdoc)

    def create_mail(self, mail, mailbox_name):
        uid = self._next_uid_for_mailbox(mailbox_name)
        new_docs = [self.soledad.create_doc(doc) for doc in mail._get_for_save(next_uid=uid)]
        self._update_index(new_docs)

    def mail(self, ident):
        fdoc = self.soledad.get_from_index('by-type-and-contenthash', 'flags', ident)[0]
        hdoc = self.soledad.get_from_index('by-type-and-contenthash', 'head', ident)[0]
        bdoc = self.soledad.get_from_index('by-type-and-payloadhash', 'cnt', hdoc.content['body'])[0]
        return PixelatedMail.from_soledad(fdoc, hdoc, bdoc, soledad_querier=self)

    def remove_mail(self, mail):
        _mail = self.mail(mail.ident)
        self.soledad.delete_doc(_mail.bdoc)
        self.soledad.delete_doc(_mail.hdoc)
        self.soledad.delete_doc(_mail.fdoc)

    def _next_uid_for_mailbox(self, mailbox_name):
        mails = self.all_mails_by_mailbox(mailbox_name)
        mails.sort(key=lambda x: x.uid, reverse=True)
        if len(mails) == 0:
            return 1
        return mails[0].uid + 1

    def _update_index(self, docs):
        db = self.soledad._db

        indexed_fields = db._get_indexed_fields()
        if indexed_fields:
            # It is expected that len(indexed_fields) is shorter than
            # len(raw_doc)
            getters = [(field, db._parse_index_definition(field))
                       for field in indexed_fields]
            for doc in docs:
                db._update_indexes(doc.doc_id, doc.content, getters, db._db_handle)
