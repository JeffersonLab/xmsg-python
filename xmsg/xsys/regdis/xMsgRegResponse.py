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
import sys

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil


class xMsgRegResponse:

    topic = str(xMsgConstants.UNDEFINED)
    sender = str(xMsgConstants.UNDEFINED)
    status = str(xMsgConstants.SUCCESS)
    data = []

    def __init__(self, topic, sender, data, status=str(xMsgConstants.SUCCESS)):
        self.topic = topic
        self.sender = sender
        self.status = status
        if data is not None:
            for d in data:
                self.data.append(d)

    @classmethod
    def create_from_multipart_request(cls, request):
        topic = request[0]
        sender = request[1]
        status = request[2]

        xMsgUtil.log("Request " + str(topic) + " had response : " + str(status))
        xMsgUtil.log("\tDetails  : ")
        xMsgUtil.log("\t-----------")
        xMsgUtil.log("\ttopic  : " + str(topic))
        xMsgUtil.log("\tsender : " + str(sender))
        xMsgUtil.log("\tstatus : " + str(status))

        try:
            data = request[3]
            xMsgUtil.log("\tdata   : True (with size : " + str(sys.getsizeof(data)) + ")")

        except IndexError:
            data = []
            xMsgUtil.log("\tdata : False")
        finally:
            return cls(topic, sender, data, status)

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
