# coding=utf-8

import threading

import zmq
from zmq.devices.proxydevice import ProcessProxy

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgExceptions import AddressInUseException
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
        host (String): proxy hostname
        port (int): proxy port

    *How to launch*
    ::
        python xmsg/sys/xMsgProxy.py

    *or*
    ::
        px_proxy
    """

    def __init__(self, context, host, port):
        """xMsgProxy Constructor

        Args:
            context (zmq.Context): zmq context object
            host (String): proxy hostname
            port (int): proxy port
        """
        self.context = context
        self.proxy_address = ProxyAddress(host, port)
        self._proxy = None
        self._controller = None

    def start(self):
        """Starts the proxy server of the xMsgNode on a local host.
        It will launch the xmsg pub-sub proxy, it will exit if another node
        running with the same address
        """
        try:
            self._controller = self._Controller(self.context,
                                                self.proxy_address)
            self._proxy = self._Proxy(self.proxy_address)

            self._controller.start()
            self._proxy.start()

        except zmq.error.ZMQError:
            raise AddressInUseException("Proxy address already being used")

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self._proxy.stop()
        self._controller.stop()

    class _Proxy(object):

        def __init__(self, proxy_address):
            super(xMsgProxy._Proxy, self).__init__()
            self._proxy_address = proxy_address
            self._proxy = None

        def start(self):
            self._proxy = ProcessProxy(zmq.XSUB, zmq.XPUB)
            self._proxy.bind_in("tcp://*:%d" % self._proxy_address.pub_port)
            self._proxy.bind_out("tcp://*:%d" % self._proxy_address.sub_port)
            self._proxy.start()
            self._proxy.join()

        def stop(self):
            zmq.Context.destroy(self._proxy.context_factory())

    class _Controller(threading.Thread):

        def __init__(self, context, proxy_address):
            super(xMsgProxy._Controller, self).__init__()
            self.daemon = True
            self._context = context
            self._is_running = threading.Event()
            self._proxy_address = proxy_address

            self._ctl_socket = self._context.socket(zmq.SUB)
            self._pub_socket = self._context.socket(zmq.PUB)

            self._ctl_socket.connect("tcp://%s:%d"
                                     % (self._proxy_address.host,
                                        self._proxy_address.sub_port))
            self._ctl_socket.setsockopt(zmq.SUBSCRIBE,
                                        xMsgConstants.CTRL_TOPIC)
            self._pub_socket.connect("tcp://%s:%d"
                                     % (self._proxy_address.host,
                                        self._proxy_address.pub_port))

            self._router_socket = self._context.socket(zmq.ROUTER)
            router_port = int(self._proxy_address.pub_port) + 2
            self._router_socket.setsockopt(zmq.ROUTER_HANDOVER, 1)
            self._router_socket.bind("tcp://*:%d" % router_port)

        def run(self):
            poller = zmq.Poller()
            poller.register(self._ctl_socket, zmq.POLLIN)
            while not self._is_running.isSet():
                try:
                    socks = dict(poller.poll(100))
                    if socks.get(self._ctl_socket) == zmq.POLLIN:
                        msg = self._ctl_socket.recv_multipart()
                        if not msg:
                            break
                        self.process_request(msg)

                except zmq.error.ZMQError as e:
                    xMsgUtil.log(e.message)

                except KeyboardInterrupt:
                    self._context.destroy()
                    return

        def stop(self):
            self._is_running.set()
            return

        def process_request(self, msg):
            topic_frame, type_frame, id_frame = msg

            if type_frame == xMsgConstants.CTRL_CONNECT:
                self._router_socket.send_multipart([id_frame, type_frame])

            elif type_frame == xMsgConstants.CTRL_SUBSCRIBE:
                self._pub_socket.send_multipart([id_frame, type_frame])

            elif type_frame == xMsgConstants.CTRL_REPLY:
                self._router_socket.send_multipart([id_frame, type_frame])

            else:
                xMsgUtil.log("unexpected request: " + str(type_frame))


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", help="Proxy address", type=str,
                        default="localhost")
    parser.add_argument("--port", help="Proxy port", type=int,
                        default=xMsgConstants.DEFAULT_PORT)

    args = parser.parse_args()
    host = args.host
    port = args.port

    try:
        proxy = xMsgProxy(zmq.Context(), host, port)
        proxy.start()
    except AddressInUseException as e:
        xMsgUtil.log(e.message)
        return


if __name__ == '__main__':
    main()
