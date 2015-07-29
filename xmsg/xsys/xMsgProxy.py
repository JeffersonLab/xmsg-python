#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil


class xMsgProxy:
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
        ./bin/unix/px_proxy
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
        self._xsub_socket = self.context.socket(zmq.XSUB)
        self._xsub_socket.set_hwm(0)
        self._xsub_socket.bind("tcp://*:%d" % int(xMsgConstants.DEFAULT_PORT))

        # socket where clients subscribe data/messages
        self._xpub_socket = self.context.socket(zmq.XPUB)
        self._xpub_socket.set_hwm(0)
        xpub_port = int(xMsgConstants.DEFAULT_PORT) + 1
        self._xpub_socket.bind("tcp://*:%d" % xpub_port)

        xMsgUtil.log("Info: Running xMsg proxy server on the localhost...")

        zmq.proxy(self._xsub_socket, self._xpub_socket, None)


def main():
    try:
        proxy = xMsgProxy(zmq.Context())
        proxy.start()

    except zmq.error.ZMQError:
        xMsgUtil.log("Cannot start proxy: address already in use...")
        return -1

    except KeyboardInterrupt:
        xMsgUtil.log("Exiting the proxy...")
        return 0

if __name__ == '__main__':
    main()
