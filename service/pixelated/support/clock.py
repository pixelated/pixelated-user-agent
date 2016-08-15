from datetime import datetime
from os.path import expanduser
from contextlib import contextmanager


class Clock():

    def __init__(self, label, user=None):
        self.start = datetime.now()
        self.label = label
        self.user = user

    def stop(self, fresh=False, user=None):
        end = datetime.now()
        flag = ' fresh-account' if fresh else ''
        with open(expanduser('~/MetricsTime'), 'a') as f:
            f.write('{} {:.5f} {} {}\n'.format((self.user or user or 'Unknown'), (end - self.start).total_seconds(), self.label, flag))


@contextmanager
def clock(label, user=None, fresh=False):
    t = Clock(label, user)
    yield
    t.stop(fresh, user)


class clock_function(object):

    def __init__(self, label, user=None, method=False):
        self.label = label
        self.user = user
        self.method = method

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            with clock(self.label, self.user):
                result = f(*args[(1 if self.method else 0):], **kwargs)
            return result
        return wrapped_f


class clock_method(clock_function):

    def __init__(self, *args, **kwargs):
        super(clock_method, self).__init__(*args, **dict(kwargs, method=True))
