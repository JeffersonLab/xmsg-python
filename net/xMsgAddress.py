from core import xMsgUtil, xMsgConstants

__author__ = 'gurjyan'

class xMsgAddress:

    """
      xMsg network address container class.
      Defines a key constructed sa host:port (xMsg
      convention) for storing xMsgConnection objects.
    """

    host = xMsgConstants.UNDEFINED
    port = xMsgConstants.DEFAULT_PORT
    key = xMsgConstants.UNDEFINED

    def __init__(self, host, port=xMsgConstants.DEFAULT_PORT):
        """
          Constructor that converts host name into a
          dotted notation of the IP address.
          It creates an instance of the cMsgAddress
          using user provided host and port. IF port
          is not defined uses default port
        :param host name
        :param port port number
        """
        self.host = xMsgUtil.host_to_ip(host)
        self.port = port
        self.key = self.host + ":" + self.port

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def setPort(self, port):
        self.port = port

    def getKey(self):
        return self.key