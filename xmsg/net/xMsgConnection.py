'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''
from xmsg.core.xMsgConstants import xMsgConstants

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
