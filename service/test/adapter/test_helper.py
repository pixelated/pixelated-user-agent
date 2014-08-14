from mock import Mock

LEAP_FLAGS = ['\\Seen',
              '\\Answered',
              '\\Flagged',
              '\\Deleted',
              '\\Draft',
              '\\Recent',
              'List']

def leap_mail(uid=0, extra_flags=[], headers={}):
  flags = LEAP_FLAGS + extra_flags
  return Mock(getUID=Mock(return_value=uid),
              getFlags=Mock(return_value=flags),
              bdoc=Mock(content={'raw': 'test'}),
              hdoc=Mock(content={'headers': headers}))
