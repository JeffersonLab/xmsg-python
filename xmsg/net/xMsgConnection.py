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

from xmsg.core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'


class xMsgConnection:
    """xMsg connection class

    Contains xMSgAddress object and two zmq socket objects for
    publishing and subscribing xMsg messages respectfully.

    Attributes:
        address (xMsgAddress): xMsg address object
        pub_sock (zmq.Socket): connection PUB socket
        sub_sock (zmq.Socket): connection SUB socket
    """

    def __init__(self, address=str(xMsgConstants.UNDEFINED)):
        self.pub_sock = str(xMsgConstants.UNDEFINED)
        self.sub_sock = str(xMsgConstants.UNDEFINED)

    def set_address(self, address):
        """Sets the connection address

        Args:
            address (xMsgAddress): xMsg address object
        """
        self.address = address

    def get_address(self):
        """Returns connection address

        Returns:
            address (xMsgAddress): connection address
        """
        return self.address

    def set_pub_sock(self, socket):
        """Returns xMsg PUB socket

        Args:
            socket (zmq.Socket): connection PUB socket
        """
        self.pub_sock = socket

    def get_pub_sock(self):
        """Returns xMsg PUB socket

        Returns:
            pub_sock (zmq.Socket): connection PUB socket
        """
        return self.pub_sock

    def set_sub_sock(self, socket):
        """Returns xMSg SUB socket

        Args:
            socket (zmq.Socket): connection SUB socket
        """
        self.sub_sock = socket

    def get_sub_sock(self):
        """Returns xMsg SUB socket

        Returns:
            sub_sock (zmq.Socket): connection SUB socket
        """
        return self.sub_sock
