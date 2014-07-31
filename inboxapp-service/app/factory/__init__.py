import inboxapp

class ProviderNotFoundException(Exception):
    def __init__(self, provider):
        self.provider = provider

    def __str__(self):
        return "Provider '%s' not found" % self.provider

class ClientFactory:

    @staticmethod
    def create(provider, account):
        if provider  == 'inboxapp':
            return inboxapp.Client(account)
        raise ProviderNotFoundException(provider)

class MailConverterFactory:

    @staticmethod
    def create(provider, client):
        if provider ==  'inboxapp':
            return inboxapp.MailConverter(client)
        raise ProviderNotFoundException(provider)

