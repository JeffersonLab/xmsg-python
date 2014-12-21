from core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'

class xMsgConnection:
    """
      xMsg connection class. Contains xMSgAddress object and
      two zmq socket objects for publishing and subscribing
      xMsg messages respectfully.
    """

    address = xMsgConstants.UNDEFINED
    pubSock = xMsgConstants.UNDEFINED
    subSock = xMsgConstants.UNDEFINED

    def __init__(self):
        pass

    def setAddress(self, ad):
        self.address = ad

    def getAddress(self):
        return self.address

    def setPubSock(self, soc):
        self.pubSock = soc

    def getPubSock(self):
        return self.pubSock

    def setSubSock(self, soc):
        self.subSock = soc

    def getSubSock(self):
        return self.subSock
