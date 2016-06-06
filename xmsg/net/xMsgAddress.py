# coding=utf-8

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil


def default_sub_port(pub_port):
    return pub_port + 1


class RegAddress(object):
    """xMsg network address container class.

    The network address of an %xMsg registrar service.
    Registration services allow discoverability of running %xMsg actors.
    By default, registrar services use localhost IP as its address,
    and xMsgConstants.REGISTRAR_PORT as the listening port.


    Attributes:
        host (String): address host
        port (int): address port
        address (String): address dotted notation
    """
    def __init__(self,
                 host="localhost",
                 port=int(xMsgConstants.REGISTRAR_PORT)):
        """Constructor that converts host name into a dotted notation
        of the IP address.

        It creates an instance of the cMsgAddress using user provided host and
        port. If port is not defined uses default port

        Args:
            hostname (String): The registrar service hostname
            port (int): The registrar port number
        """
        self.host = xMsgUtil.host_to_ip(host)
        self.port = port
        self.address = "tcp://%s:%d" % (self.host, self.port)

    def __eq__(self, other):
        return self.host == other.host and self.port == other.port

    def __str__(self):
        return self.address


class ProxyAddress(object):
    """xMsg network address container class.

    Defines a key constructed as host:port (xMsg convention) for storing
    xMsgConnection objects.

    Attributes:
        host (String): The hostname for the proxy
        pub_port (int): The publication port of the proxy
        sub_port (int): The subscription port of the proxy
    """
    def __init__(self,
                 host="localhost",
                 pub_port=int(xMsgConstants.DEFAULT_PORT),
                 sub_port=None):
        """"By default creates an address using localhost and default port if
        no parameters are given
        """
        self.host = xMsgUtil.host_to_ip(host)
        self.pub_port = pub_port
        self.sub_port = sub_port or default_sub_port(self.pub_port)

    def __eq__(self, other):
        return (self.host == other.host and self.pub_port == other.pub_port and
                self.sub_port == other.sub_port)

    def __str__(self):
        return str(self.host)
