class Client:

    def __init__(self, account):
        pass
                

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



