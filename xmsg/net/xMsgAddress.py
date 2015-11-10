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
from xmsg.core.xMsgUtil import xMsgUtil


def default_sub_port(pub_port):
    return pub_port + 1


class RegAddress(object):
    """xMsg network address container class.

    Defines a key constructed as host:port (xMsg convention) for storing
    xMsgConnection objects.

    Attributes:
        host (String): address host
        port (int): address port
        key (String): address dotted notation
    """

    def __init__(self, host="localhost", port=xMsgConstants.DEFAULT_PORT):
        """Constructor that converts host name into a dotted notation
        of the IP address.

        It creates an instance of the cMsgAddress using user provided host and
        port. If port is not defined uses default port

        Args:
            hostname (String): hostname
            port (int): port number
        """
        self.host = xMsgUtil.host_to_ip(host)
        self.port = int(port)
        self.key = "%s:%d" % (self.host, self.port)

    def get_host(self):
        """Returns the host ip address

        Returns:
            host (String): host ip address
        """
        return self.host

    def get_port(self):
        """Returns the address port

        Returns:
            port (int): host port
        """
        return self.port

    def get_key(self):
        """Returns address generated key

        Returns:
            key (String): address generated key
        """
        return self.key

    def __str__(self):
        return self.key


class ProxyAddress(object):

    def __init__(self, host="localhost", pub_port=xMsgConstants.DEFAULT_PORT,
                 sub_port=None):
        self.host = xMsgUtil.host_to_ip(host)
        self.pub_port = int(pub_port)
        self.sub_port = sub_port or default_sub_port(self.pub_port)
