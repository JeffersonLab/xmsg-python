from core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'


class xMsgConnection:
    """
      xMsg connection class. Contains xMSgAddress object and
      two zmq socket objects for publishing and subscribing
      xMsg messages respectfully.
    """

    address = str(xMsgConstants.UNDEFINED)
    pubSock = str(xMsgConstants.UNDEFINED)
    subSock = str(xMsgConstants.UNDEFINED)

    def __init__(self):
        pass

    def set_address(self, ad):
        self.address = ad

    def get_address(self):
        return self.address

    def set_pub_sock(self, soc):
        self.pubSock = soc

    def get_pub_sock(self):
        return self.pubSock

    def set_sub_sock(self, soc):
        self.subSock = soc

    def get_sub_sock(self):
        return self.subSock
