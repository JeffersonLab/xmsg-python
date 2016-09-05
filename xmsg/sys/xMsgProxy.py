# coding=utf-8

import threading
import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.net.xMsgAddress import ProxyAddress


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
        python xmsg/sys/xMsgProxy.py

    *or*
    ::
        px_proxy
    """

    def __init__(self, context, host, port):
        """
        xMsgProxy Constructor

        Args:
            context (zmq.Context): zmq context object

        Returs:
            xMsgProxy object
        """
        self.context = context
        self.proxy_address = ProxyAddress(host, port)
        self._proxy = None
        self._controller = None

    def start(self):
        """Starts the proxy server of the xMsgNode on a local host.
        It will launch the xmsg pub-sub proxy, it will exit if another node
        running with the same address

        Usage:
        ::
            python xmsg/sys/xMsgProxy.py
        """
        self._proxy = self._Proxy(self.context, self.proxy_address)
        self._controller = self._Controller(self.context, self.proxy_address)
        try:
            self._proxy.start()
            self._controller.start()

            self._proxy.join()
            self._controller.join()

        except KeyboardInterrupt:
            self._stop()

        except Exception as e:
            xMsgUtil.log(e.message)
            return -1

    def _stop(self):
        self._proxy.terminate()
        self._controller.terminate()
        xMsgUtil.log("proxy process terminated.")

    class _Proxy(threading.Thread):

        def __init__(self, context, proxy_address):
            super(xMsgProxy._Proxy, self).__init__()
            self._context = context
            self._proxy_address = proxy_address
            self._state = threading.Event()
            self._in_socket = self._context.socket(zmq.XSUB)
            self._in_socket.set_hwm(0)
            self._in_socket.bind("tcp://*:%d" % self._proxy_address.pub_port)

            # socket where clients subscribe data/messages
            self._out_socket = self._context.socket(zmq.XPUB)
            self._out_socket.set_hwm(0)
            self._out_socket.bind("tcp://*:%d" % self._proxy_address.sub_port)

        def run(self):
            xMsgUtil.log("running on host = %s port = %d"
                         % (self._proxy_address.host,
                            self._proxy_address.pub_port))
            zmq.proxy(self._in_socket, self._out_socket, None)

    class _Controller(threading.Thread):

        def __init__(self, context, proxy_address):
            super(xMsgProxy._Controller, self).__init__()
            self._context = context
            self._is_running = threading.Event()
            self._proxy_address = proxy_address

            self._ctl_socket = self._context.socket(zmq.SUB)
            self._pub_socket = self._context.socket(zmq.PUB)

            self._ctl_socket.connect("tcp://%s:%d"
                                     % (self._proxy_address.host,
                                        self._proxy_address.sub_port))
            self._ctl_socket.setsockopt(zmq.SUBSCRIBE,
                                        str(xMsgConstants.CTRL_TOPIC))
            self._pub_socket.connect("tcp://%s:%d"
                                     % (self._proxy_address.host,
                                        self._proxy_address.pub_port))

            self._router_socket = self._context.socket(zmq.ROUTER)
            router_port = int(self._proxy_address.pub_port) + 2
            self._router_socket.setsockopt(zmq.ROUTER_HANDOVER, 1)
            self._router_socket.bind("tcp://*:%d" % router_port)

        def run(self):
            while not self._is_running.is_set():
                try:
                    msg = self._ctl_socket.recv_multipart()
                    if not msg:
                        break
                    self.process_request(msg)

                except zmq.error.ZMQError as e:
                    xMsgUtil.log(e.message)

        def stop(self):
            self._is_running.set()
            return

        def process_request(self, msg):
            topic_frame, type_frame, id_frame = msg

            if type_frame == str(xMsgConstants.CTRL_CONNECT):
                self._router_socket.send_multipart([id_frame, type_frame])

            elif type_frame == str(xMsgConstants.CTRL_SUBSCRIBE):
                self._pub_socket.send_multipart([id_frame, type_frame])

            elif type_frame == str(xMsgConstants.CTRL_REPLY):
                self._router_socket.send_multipart([id_frame, type_frame])

            else:
                xMsgUtil.log("unexpected request: " + str(type_frame))

    class _Listener(threading.Thread):

        def __init__(self):
            super(xMsgProxy._Listener, self).__init__()


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", help="Proxy address", type=str,
                        default="localhost")
    parser.add_argument("--port", help="Proxy port", type=int,
                        default=int(xMsgConstants.DEFAULT_PORT))

    args = parser.parse_args()
    host = args.host
    port = args.port

    proxy = xMsgProxy(zmq.Context(), host, port)
    proxy.start()

if __name__ == '__main__':
    main()
