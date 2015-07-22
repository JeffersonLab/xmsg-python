'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''
import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil


class xMsgProxy:
    """
    Runs xMsg pub-sub proxy.
    This is a simple stateless message switch, i.e. a device that forwards
    messages without inspecting them. This simplifies dynamic discovery problem
    All xMsg clients (publishers and subscribers) connect to the proxy, instead
    of to each other. It becomes trivial to add more subscribers or publishers.
    """

    context = str(xMsgConstants.UNDEFINED)

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
        """
        Starts the proxy server of the xMsgNode on a local host.
        """
        self.d_sub = self.context.socket(zmq.XSUB)
        self.d_sub.set_hwm(0)
        self.d_sub.bind("tcp://%s:%s" % (str("*"),
                                         str(int(xMsgConstants.DEFAULT_PORT))))

        # socket where clients subscribe data/messages
        self.d_pub = self.context.socket(zmq.XPUB)
        self.d_pub.set_hwm(0)
        self.d_pub.bind("tcp://%s:%s" % (str("*"),
                                         str(int(xMsgConstants.DEFAULT_PORT) + 1)))

        xMsgUtil.log("Info: Running xMsg proxy server on the localhost...")

        zmq.proxy(self.d_sub, self.d_pub, None)


def main():
    try:
        proxy = xMsgProxy(zmq.Context())
        proxy.start()

    except:
        return

if __name__ == '__main__':
    main()
