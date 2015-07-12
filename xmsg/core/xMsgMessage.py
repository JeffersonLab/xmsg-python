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
from xmsg.data import xMsgMeta_pb2, xMsgData_pb2
from xmsg.core.xMsgExceptions import MessageException

__author__ = 'gurjyan'


class xMsgMessage():
    """
    Defines a message to be serialized and passed through 0MQ.

    Uses {@link xMsgData} class generated as a result of the proto-buffer
    description to pass Java primitive types and arrays of primitive types.
    xMsgData is also used to pass byte[]: the result of a user specific
    object serialization.
    <p>
    This class will also contain complete metadata of the message data,
    describing details of the data. In case an object is constructed
    without a metadata, the default metadata will be created and the
    proper data type will set based on the passed data parameter type.
    <p>
    Note that data that is an instance of {@code byte[]} will be considered to be
    a serialization of a specific user object only in the case when a proper

    @author gurjyan
    @version 2.x
    @since 16/6/15
    """
    topic = str(xMsgConstants.UNDEFINED)
    metadata = str(xMsgConstants.UNDEFINED)
    data = str(xMsgConstants.UNDEFINED)

    def __init__(self, topic, serialized_data=None):
        self.topic = topic
        if(isinstance(serialized_data, basestring)
           or isinstance(serialized_data, bytearray)
           or isinstance(serialized_data, bytes)):
            self.data = serialized_data
        else:
            raise TypeError("xMsgMessage: Constructor only accepts serialized data")

    @classmethod
    def create_with_xmsg_data(cls, topic, xmsg_data_object):
        if isinstance(xmsg_data_object, xMsgData_pb2.xMsgData):
            return cls(topic, xmsg_data_object.SerializeToString())
        else:
            raise TypeError("xMsgMessage: Invalid type of data object")

    @classmethod
    def create_with_serialized_data(cls, topic, serialized_data):
        return cls(topic, serialized_data)

    def get_data(self):
        """
        Returns data field as python bytes
        """
        return self.data

    def get_metadata(self):
        """
        Returns metadata object (xMsgMeta)
        """
        return self.metadata

    def get_metadata_bytes(self):
        """
        Returns metadata as python bytes
        """
        if isinstance(self.get_metadata(), xMsgMeta_pb2.xMsgMeta):
            try:
                return self.metadata.SerializeToString()
            except:
                return bytes(self.metadata)
        else:
            raise MessageException("xMsgMessage: User needs to define metadata")
            return

    def mimetype(self, mimetype):
        return self.mimetype

    def msg(self):
        """
        Returns the msg
        """
        return [bytes(self.get_topic()), self.get_metadata_bytes(), self.get_data()]

    def get_topic(self):
        """
        Returns the topic string
        """
        return self.topic

    def set_metadata(self, metadata):
        self.metadata = metadata

    def set_mimetype(self, mimetype):
        self.mimetype = mimetype
