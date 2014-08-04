
class Client:
    def __init__(self, config, username, password, server_name, mailbox_name):
        try:
            self.username = username
            self.password = password
            self.server_name = server_name
            self.mailbox_name = mailbox_name
            self.leapdir = '%s/leap' % config.workdir

            self._open_leap_session()
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def _open_leap_session(self):
        self.leap_config = LeapConfig(leap_home=self.leapdir)
        self.provider = LeapProvider(self.server_name, self.leap_config)
        self.leap_session = LeapSessionFactory(self.provider).create(LeapCredentials(self.username, self.password))
        self.mbx = self.leap_session.account.getMailbox(self.mailbox_name)


    def mails(self, query):
        raise NotImplementedError()


    def drafts(self):
        raise NotImplementedError()


    def mail(self, mail_id):
        raise NotImplementedError()


    def thread(self, thread_id):
        raise NotImplementedError()


    def mark_as_read(self, mail_id):
        raise NotImplementedError()


    def tags_for_thread(self, thread):
        raise NotImplementedError()


    def add_tag_to_thread(self, thread_id, tag):
        raise NotImplementedError()


    def remove_tag_from_thread(self, thread_id, tag):
        raise NotImplementedError()


    def delete_mail(self, mail_id):
        raise NotImplementedError()


    def save_draft(self, draft):
        raise NotImplementedError()


    def send_draft(self, draft):
        raise NotImplementedError()


    def draft_reply_for(self, mail_id):
        raise NotImplementedError()


    def all_tags(self):
        raise NotImplementedError()


    def all_contacts(self, query):
        raise NotImplementedError()
