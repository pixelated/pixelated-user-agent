import signal
import sys
from threading import Thread
from twisted.internet import reactor
import logging


def signal_handler(signal, frame):
        stop_reactor_on_exit()
        sys.exit(0)


def start_reactor(logging=False):
    if logging:
        enable_logging()

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


def enable_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='/tmp/leap.log',
                        filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
