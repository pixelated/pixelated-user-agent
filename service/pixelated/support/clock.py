from datetime import datetime
from os.path import expanduser

class Clock():

    def __init__(self, label):
        self.start = datetime.now()
        self.label = label

    def stop(self, fresh=False):
        end = datetime.now()
        with open(expanduser('~/MetricsTime'), 'a') as f:
            flag = ' fresh-account' if fresh else ''
            f.write('{} {:.5f}{}\n'.format(self.label, (end - self.start).total_seconds(), flag))
