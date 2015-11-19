#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
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

from xmsg.core.xMsgConstants import xMsgConstants as constants
from xmsg.net.xMsgConnection import xMsgConnection
from xmsg.net.xMsgConnectionSetup import xMsgConnectionSetup
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver


class ConnectionManager:
    context = str(constants.UNDEFINED)
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

    def release_registrar_connection(self, connection):
        connection.destroy()

    def release_proxy_connection(self, connection):
        self.context.destroy(connection.get_pub_socket())
        self.context.destroy(connection.get_sub_socket())

    def destroy(self):
        self.context.destroy()
