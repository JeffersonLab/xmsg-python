#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from xmsg.core.xMsgExceptions import BadRequest
from xmsg.data import xMsgRegistration_pb2


class xMsgRegRequest:
    """A wrapper for a a registration or discovery request.

    Attributes:
        topic (String): Request topic
        sender (String): sender of the xMsg request
        data (bytes[]): serialized data included in the message
            (text or registration data)
    """

    def __init__(self, topic, sender, data):
        '''
        topic (String): Request topic
        sender (String): sender of the xMsg request
        data (bytes[]): serialized data included in the message
            (text or registration data)
        '''
        self.topic = topic
        self.sender = sender
        if isinstance(data, xMsgRegistration_pb2.xMsgRegistration):
            self.data = data.SerializeToString()
        else:
            self.data = data

    @classmethod
    def create_from_multipart(cls, multipart_request):
        """Constructs RegRequest serialized message object

        Args:
            multipart_request (list): multipart zmq message

        Returns:
            xMsgRegRequest: xmsg request object

        Raises:
            BadRequest: if the message is corrupted or malformed
        """
        try:
            return cls(multipart_request[0],
                       multipart_request[1],
                       multipart_request[2])

        except IndexError:
            raise BadRequest("Malformed request message")

    def msg(self):
        """Serialize the content of the request

        Returns:
            bytes[]: serialized message for zeromq
        """
        return [str(self.topic), str(self.sender), self.data]
