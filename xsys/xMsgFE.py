import signal

import zmq

from core.xMsgConstants import xMsgConstants
from xsys.regdis.xMsgRegistrar import xMsgRegistrar


__author__ = 'gurjyan'


class xMsgFE():
    """
    xMsg Front-End
    """

    context = str(xMsgConstants.UNDEFINED)

    def __init__(self):

        # create a zmq context
        self.context = zmq.Context()

        # Start local registrar service. Constructor starts a thread
        # that periodically updates front-end registrar database with
        # the data from the local databases
        self.t = xMsgRegistrar(self.context)
        self.t.daemon = True
        self.t.start()

    def exit_gracefully(self, signum, frame):
        print "xMsgFE death"
        self.context.close()

    def join(self):
        self.t.join()


def main():
    xn = xMsgFE()
    signal.signal(signal.SIGTERM, xn.exit_gracefully)
    signal.signal(signal.SIGINT, xn.exit_gracefully)

if __name__ == '__main__':
    main()
