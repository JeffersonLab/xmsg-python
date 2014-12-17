import signal

import zmq

from core import xMsgConstants
from xsys.regdis.xMsgRegistrar import xMsgRegistrar


__author__ = 'gurjyan'

class xMsgFE():
    """
    xMsg Front-End
    """

    context = xMsgConstants.UNDEFINED

    def __init__(self):

        # create a zmq context
        self.context = zmq.Context()

        # Start local registrar service. Constructor starts a thread
        # that periodically updates front-end registrar database with
        # the data from the local databases
        t = xMsgRegistrar(self.context)
        t.daemon = True
        t.start()

    def exit_gracefully(self, signum, frame):
        self.context.close()

def main():
    xn = xMsgFE()
    signal.signal(signal.SIGTERM, xn.exit_gracefully)
    signal.signal(signal.SIGINT, xn.exit_gracefully)

if __name__ == '__main__':
    main()
