from core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'


class xMsgMessage():

    def __init__(self, author=str(xMsgConstants.UNDEFINED),
                 domain=str(xMsgConstants.UNDEFINED),
                 subject=str(xMsgConstants.UNDEFINED),
                 xtype=str(xMsgConstants.UNDEFINED),
                 data=str(xMsgConstants.UNDEFINED)):

        self.author = author
        self.domain = domain
        self.subject = subject
        self.xtype = xtype
        self.data = data

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_domain(self):
        return self.domain

    def set_domain(self, domain):
        self.domain = domain

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_type(self):
        return self.xtype

    def set_type(self, xtype):
        self.xtype = xtype

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
