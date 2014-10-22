import getpass


def run():
    provider = raw_input('Which provider do you want to connect to:\n')
    username = raw_input('What\'s your username registered on the provider:\n')
    password = getpass.getpass('Type your password:\n')
    return provider, username, password
