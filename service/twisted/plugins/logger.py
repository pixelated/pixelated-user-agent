import gc
import sys

from zope.interface import implementer
from twisted.plugin import IPlugin
from loglinegenerator import ILogLineGenerator


@implementer(IPlugin, ILogLineGenerator)
class GCLogger():
    def getLogLine(self):
        return '%010d' % sum(sys.getsizeof(o) for o in gc.get_objects())


gcLogger = GCLogger()
