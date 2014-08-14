import signal
import sys
from threading import Thread
from twisted.internet import reactor


def signal_handler(signal, frame):
        stop_reactor_on_exit()
        sys.exit(0)


def start_reactor():
    def start_reactor_run():
        reactor.run(False)

    global REACTOR_THREAD
    REACTOR_THREAD = Thread(target=start_reactor_run)
    REACTOR_THREAD.start()


def stop_reactor_on_exit():
    reactor.callFromThread(reactor.stop)
    global REACTOR_THREAD
    REACTOR_THREAD = None

signal.signal(signal.SIGINT, signal_handler)
