# coding=utf-8

import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.net.xMsgConnection import xMsgConnection
from xmsg.net.xMsgConnectionSetup import xMsgConnectionSetup
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver


class ConnectionManager:
    context = str(xMsgConstants.UNDEFINED)
    default_setup = xMsgConnectionSetup()

    def __init__(self, context):
        self.context = context

    def get_proxy_connection(self, address, connection_setup):
        """
        Args:
            address (ProxyAddress): Proxy address object
            connection_setup (xMsgConnectionSetup): Connection setup
        """
        pub_socket = self.context.socket(zmq.PUB)
        sub_socket = self.context.socket(zmq.SUB)

        connection_setup.pre_connection(pub_socket)
        connection_setup.pre_connection(sub_socket)

        pub_port = address.pub_port
        sub_port = address.sub_port

        pub_socket.connect("tcp://%s:%d" % (address.host, pub_port))
        sub_socket.connect("tcp://%s:%d" % (address.host, sub_port))

        connection_setup.post_connection()

        return xMsgConnection(address, pub_socket, sub_socket)

    def get_registrar_connection(self, registration_address):
        return xMsgRegDriver(self.context, registration_address)

    @staticmethod
    def release_registrar_connection(connection):
        connection.destroy()

    def release_proxy_connection(self, connection):
        self.context.destroy(connection.pub_socket)
        self.context.destroy(connection.sub_socket)

    def destroy(self):
        self.context.destroy()
