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
from core.xMsgExceptions import BadRequest
from data import xMsgRegistration_pb2


class xMsgRegRequest:

    topic = str(xMsgConstants.UNDEFINED)
    sender = str(xMsgConstants.UNDEFINED)
    data = str(xMsgConstants.UNDEFINED)

    def __init__(self, topic=None, sender=None, data=None):
        '''
        :param topic: Request topic
        :param sender: sender of the xMsg request
        :param data: data included in the message (text or registration)
        '''
        self.topic = topic
        self.sender = sender
        self.data = data

    @classmethod
    def create_from_multipart_request(cls, multipart_request):
        """
        Initialize RegRequest serialized message
        """
        try:
            return cls(multipart_request[0],
                       multipart_request[1],
                       multipart_request[2])
        except:
            raise BadRequest("Malformed request message")

    def get_topic(self):
        """
        Gets the topic of the request
        """
        return str(self.topic)

    def get_sender(self):
        """
        Gets the sender of the request
        """
        return str(self.sender)

    def get_data(self):
        """
        Get registration data object
        """
        r_data = xMsgRegistration_pb2.xMsgRegistration()
        r_data.ParseFromString(self.data)
        return r_data

    def get_serialized_msg(self):
        """
        Serialize the content of the request
        """
        return [str(self.topic), str(self.sender), str(self.data)]
