# coding=utf-8

import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.xsys.pubsub.IdentityGenerator import IdentityGenerator


class xMsgProxyDriver(object):

    def __init__(self, proxy_address):
        """ xMsgProxyDriver constructor
        Args:
            proxy_address (ProxyAddress):
        """
        self._address = proxy_address
        self._identity = str(IdentityGenerator.get_ctrl_id())
        self._context = zmq.Context()
        self._pub_socket = self._sub_socket = self._ctl_socket = None
        try:
            self._pub_socket = self._context.socket(zmq.PUB)
            self._sub_socket = self._context.socket(zmq.SUB)
            self._ctl_socket = self._context.socket(zmq.DEALER)

        except Exception as e:
            del self._sub_socket
            del self._pub_socket
            raise e

        self._ctl_socket.identity = self._identity

    def get_address(self):
        """ returns proxy address

        Returns:
            ProxyAddress: proxy address object
        """
        return self._address

    def get_pub_socket(self):
        """ returns publisher socket

        Returns:
            zmq.Socket
        """
        return self._pub_socket

    def get_sub_socket(self):
        """ returns subscriber socket

        Returns:
            zmq.Socket
        """
        return self._sub_socket

    def connect(self):
        """ Connects the publisher, subscriber and ctrl sockets to start messaging
        """
        ctrl_port = self._address.sub_port + 1
        self._pub_socket.connect("tcp://%s:%d" % (self._address.host,
                                                  self._address.pub_port))
        self._sub_socket.connect("tcp://%s:%d" % (self._address.host,
                                                  self._address.sub_port))
        self._ctl_socket.connect("tcp://%s:%d" % (self._address.host,
                                                  ctrl_port))

    def check_connection(self):
        retries = 0
        max_retries = 20

        connection_poller = zmq.Poller()
        connection_poller.register(self._ctl_socket, zmq.POLLIN)

        while retries < max_retries:

            try:
                serialized_msg = [str(xMsgConstants.CTRL_TOPIC) + ":con",
                                  str(xMsgConstants.CTRL_CONNECT),
                                  str(self._identity)]
                self._send(serialized_msg)

                socks = dict(connection_poller.poll(100))
                if socks.get(self._ctl_socket) == zmq.POLLIN:
                    t_data = self._ctl_socket.recv_multipart()

                    if len(t_data) == 1:
                        if t_data[0] == str(xMsgConstants.CTRL_CONNECT):
                            return True
                retries += 1

            except zmq.ZMQError as e:
                print e.message
                return False
        return False

    def subscribe(self, topic):
        self._sub_socket.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe(self, topic):
        self._sub_socket.setsockopt(zmq.UNSUBSCRIBE, topic)

    def check_subscription(self, topic):
        retries = 0
        max_retries = 20

        connection_poller = zmq.Poller()
        connection_poller.register(self._sub_socket, zmq.POLLIN)

        while retries < max_retries:

            try:
                serialized_msg = [str(xMsgConstants.CTRL_TOPIC) + ":sub",
                                  str(xMsgConstants.CTRL_SUBSCRIBE),
                                  str(topic)]
                self._send(serialized_msg)

                socks = dict(connection_poller.poll(100))
                if socks.get(self._sub_socket) == zmq.POLLIN:
                    t_data = self._sub_socket.recv_multipart()

                    if len(t_data) == 2:
                        m_id = t_data[0]
                        m_type = t_data[1]
                        if m_type == str(xMsgConstants.CTRL_SUBSCRIBE) and m_id == topic:
                            return True
                retries += 1
            except zmq.ZMQError as e:
                print e.message
                return False
        return False

    def send(self, message):
        self._pub_socket.send(message.topic, zmq.SNDMORE)
        self._pub_socket.send(message.metadata.SerializeToString(), zmq.SNDMORE)
        self._pub_socket.send(message.data)

    def _send(self, serialized_message):
        self._pub_socket.send(serialized_message[0], zmq.SNDMORE)
        self._pub_socket.send(serialized_message[1], zmq.SNDMORE)
        self._pub_socket.send(serialized_message[2])

    def recv(self):
        return self._sub_socket.recv_multipart()

    def close(self, linger):
        pass
