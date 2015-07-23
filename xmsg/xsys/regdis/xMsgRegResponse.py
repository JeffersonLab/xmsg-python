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


class xMsgRegResponse:
    """A wrapper for a response to a registration or discovery request.

    A response of the xMsgRegService registration service can be an string
    indicating that the request was successful, a set of registration data
    in case a discovery request was received, or an error description
    indicating that something wrong happened with the request.

    Attributes:
        topic (string): topic of the response message
        sender (string): response sender
        status (string): status of the request to respond
        data (bytesarray): registration datas
    """
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
        """Returns (creates) a response object from multipart request"""
        topic = request[0]
        sender = request[1]
        status = request[2]

        try:
            data = request[3]

        except IndexError:
            data = []

        finally:
            return cls(topic, sender, data, status)

    def get_topic(self):
        """Returns topic (string) in the response"""
        return str(self.topic)

    def set_topic(self, topic):
        """Sets the topic in the response

        Args:
            topic (xMsgTopic): topic for the response
        """
        self.topic = topic

    def get_sender(self):
        """Returns the sender in the response"""
        return str(self.sender)

    def set_sender(self, sender):
        """Sets the sender in the response

        Args:
            sender (string): name of sender
        """
        self.sender = sender

    def get_status(self):
        """Returns request response status

        It can be xMsgConstants#SUCCESS or an error string indicating
        a problem with the request.
        """
        return str(self.status)

    def set_status(self, status):
        """Sets the status in the response

        Args:
            status (string): status by default is ```success``` otherwise
                an string indicating the error in the request
        """
        self.status = status

    def get_data(self):
        """Returns response data array"""
        if len(self.data) is 0:
            return ""
        else:
            return self.data

    def get_serialized_msg(self):
        """Returns the response instance serialized"""
        s_msg = [self.get_topic(), self.get_sender(), self.get_status()]

        for d in self.data:
            s_msg.append(str(d))
        return s_msg
