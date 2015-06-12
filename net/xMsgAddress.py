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
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil

__author__ = 'gurjyan'


class xMsgAddress:

    """
      xMsg network address container class.
      Defines a key constructed as host:port (xMsg
      convention) for storing xMsgConnection objects.
    """

    host = str(xMsgConstants.UNDEFINED)
    port = int(xMsgConstants.DEFAULT_PORT)
    key = str(xMsgConstants.UNDEFINED)

    def __init__(self, host="localhost", port=int(xMsgConstants.DEFAULT_PORT)):
        """
          Constructor that converts host name into a
          dotted notation of the IP address.
          It creates an instance of the cMsgAddress
          using user provided host and port. If port
          is not defined uses default port
        :param host name
        :param port port number
        """
        self.host = xMsgUtil.host_to_ip(host)
        self.port = port
        self.key = self.host + ":" + str(self.port)

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_key(self):
        return self.key
