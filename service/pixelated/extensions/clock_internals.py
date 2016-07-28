from pixelated.support.clock import Clock
from leap.mail.incoming.service import IncomingMail

def _sync_soledad_with_clock(funct):
    def wrapper(*args, **kwargs):
        t1 = Clock('recurrent-sync')
        def after(param):
            t1.stop()
            return param
        d = funct(*args, **kwargs)
        d.addCallbacks(after,after)
        return d
    return wrapper

IncomingMail._sync_soledad = _sync_soledad_with_clock(IncomingMail._sync_soledad)
