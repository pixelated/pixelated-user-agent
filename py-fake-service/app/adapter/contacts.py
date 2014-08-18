import re


class Contacts:

    def __init__(self):
        self.contacts = []

    def add(self, mbox_mail):
        contact = mbox_mail.get_from()
        self.contacts.append(Contact(contact))

    def search(self, query):
        contacts_query = re.compile(query)
        return [
            contact.__dict__ for contact in self.contacts if contacts_query.match(
                contact.addresses[0])]


class Contact:

    def __init__(self, contact):
        self.addresses = [contact]
        self.name = ''
