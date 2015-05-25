import os
import signal
import sys

import zmq

from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from xsys.regdis.xMsgRegDiscDriver import xMsgRegDiscDriver
from xsys.regdis.xMsgRegistrar import xMsgRegistrar


__author__ = 'gurjyan'


class xMsgNode(xMsgRegDiscDriver):
    """
    xMsgNode.
    Runs xMsg pub-sub proxy.
    This is a simple stateless message switches, i.e. a device that
    forwards messages without inspecting them. This simplifies dynamic
    discovery problem. All xMsg clients (publishers and subscribers)
    connect to the proxy, instead of to each other. It becomes trivial
    to add more subscribers or publishers.

    """
    context = xMsgConstants.UNDEFINED
    host = xMsgConstants.UNDEFINED

    def __init__(self, feHost=None):
        """
        Starts a local registrar service.
        Constructor of the xMsgRegistrar class
        will start a thread that will periodically report local registration
        database to xMsgFE registrar service.
        This ways registration data is distributed/duplicated between xMsgNode
        and xMsgFE registrar services.
        That is the reason we need to pass xMsg front-end host name.
        Note: this version assumes that xMsgNode and xMsgFE registrar services
                  use default registrar port:
                 (xMsgConstants#REGISTRAR_PORT)

        :param feHost: xMsg front-end host. Host is passed through command line
                       -h option, or through the environmental variable:
                       XMSG_FE_HOST
        """
        xMsgRegDiscDriver.__init__(self, feHost)

        # create a zmq context
        self.context = zmq.Context()

        # local host ip
        self.host = xMsgUtil.host_to_ip("localhost")

        # Start local registrar service in a separate thread.
        # If fe host is defined the specific constructor starts a thread
        # that periodically updates front-end registrar database with
        # the data from the local databases
        self.t = xMsgRegistrar(self.context, feHost)
        self.t.daemon = True
        self.t.start()

        print (" Info: xMsg local registration and discovery server is started")

        # setting up the xMsg proxy
        # socket where clients publish their data/messages
        self.d_sub = self.context.socket(zmq.XSUB)
        self.d_sub.bind("tcp://%s:%s" % (str("*"),
                                         str(xMsgConstants.DEFAULT_PORT.get_int_value())))

        # socket where clients subscribe data/messages
        self.d_pub = self.context.socket(zmq.XPUB)
        self.d_pub.bind("tcp://%s:%s" % (str("*"),
                                         str(int(xMsgConstants.DEFAULT_PORT) + 1)))

        print (" Info: Running xMsg proxy server on the localhost...")

        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGINT, self.exit_gracefully)

        try:
            # setup the proxy
            zmq.proxy(self.d_sub, self.d_pub, None)

        except Exception, e:
            print " "
            print " "+str(e)
            print " Bringing down xMsgNode..."
        finally:
            pass

    def join(self):
        self.t.join()

    def exit_gracefully(self, signum, frame):
        # self.remove_all_registration_fe(self.host,
        #                                 str(xMsgConstants.UNDEFINED))
        self.context.destroy()


def main():
    if len(sys.argv) == 3:
        if str(sys.argv[0]) == "-h":
            xn = xMsgNode(str(sys.argv[2]))
            xn.join()
        else:
            print "wrong option. Accepts -h option only."
            os.exit(0)
    elif len(sys.argv) == 1:
            xn = xMsgNode()
            xn.join()


if __name__ == '__main__':
    main()
