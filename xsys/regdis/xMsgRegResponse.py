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
import sys


class xMsgRegResponse:

    topic = str(xMsgConstants.UNDEFINED)
    sender = str(xMsgConstants.UNDEFINED)
    status = str(xMsgConstants.SUCCESS)
    data = []

    def __init__(self, topic=None, sender=None, data=None):
        self.topic = topic
        self.sender = sender
        if data is not None:
            for d in data:
                self.data.append(d)

    def init_from_request(self, request):
        self.topic = request[0]
        self.sender = request[1]
        self.status = request[2]

        xMsgUtil.log("Request " + str(self.topic) + " had response : " + str(self.status).capitalize())
        xMsgUtil.log("\tDetails  : ")
        xMsgUtil.log("\t-----------")
        xMsgUtil.log("\ttopic  : " + str(self.topic))
        xMsgUtil.log("\tsender : " + str(self.sender))
        xMsgUtil.log("\tstatus : " + str(self.status))

        try:
            self.data = request[3]
            xMsgUtil.log("\tdata   : True (with size : " + str(sys.getsizeof(self.data)) + ")")

        except IndexError:
            self.data = []
            xMsgUtil.log("\tdata : False")

    def get_topic(self):
        return str(self.topic)

    def set_topic(self, topic):
        self.topic = topic

    def get_sender(self):
        return str(self.sender)

    def set_sender(self, sender):
        self.sender = sender

    def get_status(self):
        return str(self.status)

    def set_status(self, status):
        self.status = status

    def get_data(self):
        if len(self.data) is 0:
            return ""
        else:
            return self.data

    def get_serialized_msg(self):
        s_msg = [self.get_topic(), self.get_sender(), self.get_status()]
        for d in self.data:
            s_msg.append(str(d))
        return s_msg
