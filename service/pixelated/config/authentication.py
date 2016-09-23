class Authentication(object):

    def __init__(self, username, token, uuid, session_id, user_attributes):
        self.username = username
        self.token = token
        self.uuid = uuid
        self.session_id = session_id
        self._user_attributes = user_attributes

    def is_admin(self):
        return self._user_attributes.get('is_admin', False)
