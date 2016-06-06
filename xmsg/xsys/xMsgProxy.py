# coding=utf-8

import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil


class xMsgProxy(object):
    """Runs xMsg pub-sub proxy.

    This is a simple stateless message switch, i.e. a device that forwards
    messages without inspecting them. This simplifies dynamic discovery problem
    All xMsg clients (publishers and subscribers) connect to the proxy, instead
    of to each other. It becomes trivial to add more subscribers or publishers.

    Attributes:
        context (zmq.Context): proxy instance context

    *How to launch*
    ::
        python xmsg/xsys/xMsgProxy.py

    *or*
    ::
        px_proxy
    """

    def __init__(self, context):
        """
        xMsgProxy Constructor

        Args:
            context (zmq.Context): zmq context object

        Returs:
            xMsgProxy object
        """
        self.context = context

    def start(self):
        """Starts the proxy server of the xMsgNode on a local host.
        It will launch the xmsg pub-sub proxy, it will exit if another node
        running with the same address

        Usage:
        ::
            python xmsg/xsys/xMsgProxy.py
        """
        try:
            self._xsub_socket = self.context.socket(zmq.XSUB)
            self._xsub_socket.set_hwm(0)
            default_port = int(xMsgConstants.DEFAULT_PORT)
            self._xsub_socket.bind("tcp://*:%d" % default_port)

            # socket where clients subscribe data/messages
            self._xpub_socket = self.context.socket(zmq.XPUB)
            self._xpub_socket.set_hwm(0)
            self._xpub_socket.bind("tcp://*:%d" % (default_port + 1))

            xMsgUtil.log("Info: Running xMsg proxy server on the localhost...")

            zmq.proxy(self._xsub_socket, self._xpub_socket, None)

        except zmq.error.ZMQError:
            xMsgUtil.log("Cannot start proxy: address already in use...")
            return -1


def main():
    try:
        proxy = xMsgProxy(zmq.Context())
        proxy.start()

    except KeyboardInterrupt:
        xMsgUtil.log("Exiting the proxy...")
        return 0

if __name__ == '__main__':
    main()
