from core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'

class xMsgMessage():

    def __init__(self, author=xMsgConstants.UNDEFINED,
                 domain=xMsgConstants.UNDEFINED,
                 subject=xMsgConstants.UNDEFINED,
                 xtype=xMsgConstants.UNDEFINED,
                 data=xMsgConstants.UNDEFINED):

        self.author = author
        self.domain = domain
        self.subject = subject
        self.xtype = xtype
        self.data = data

    def getAuthor(self):
        return self.author

    def setAuthor(self, author):
        self.author = author

    def getDomain(self):
        return self.domain

    def setDomain(self, domain):
        self.domain = domain

    def getSubject(self):
        return self.subject

    def setSubject(self, subject):
        self.subject = subject

    def getType(self):
        return self.xtype

    def setType(self, xtype):
        self.xtype = xtype

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data



