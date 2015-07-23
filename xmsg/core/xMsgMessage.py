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
from xmsg.data import xMsgMeta_pb2, xMsgData_pb2

__author__ = 'gurjyan'


class xMsgMessage():
    """Defines a message to be serialized and passed through 0MQ.

    Uses xMsgData class generated as a result of the proto-buffer
    description to pass Python primitive types and arrays of primitive types.
    xMsgData is also used to pass byte[]: the result of a user specific
    object serialization.

    This class also contains complete metadata of the message data,
    describing details of the data. In case an object is constructed
    without a metadata, the default metadata will be created and the
    proper data type will set based on the passed data parameter type.

    Attributes:
        topic (xMsgTopic): topic of the message

        metadata (xMsgMeta): metadata of the message

        data (bytes[]): serialized data object

    @author gurjyan
    @version 2.x
    @since 16/6/15
    """
    topic = str(xMsgConstants.UNDEFINED)
    metadata = xMsgMeta_pb2.xMsgMeta()
    data = str(xMsgConstants.UNDEFINED)

    def __init__(self, topic, serialized_data=None):
        self.topic = topic
        if(isinstance(serialized_data, basestring) or
           isinstance(serialized_data, bytearray) or
           isinstance(serialized_data, bytes)):
            self.data = serialized_data
        else:
            raise TypeError("xMsgMessage: Constructor only"
                            " accepts serialized data")

    @classmethod
    def create_with_xmsg_data(cls, topic, xmsg_data_object):
        """
        Constructs a message with an unserialized xMsgData object and
        the default metadata

        Args:
            topic (xMsgTopic): the topic of the message

            xmsg_data_object (xMsgData): the xMsgData object unserialized
        Returns:
            xMsgMessage: xMsg message object

        Raises:
            TypeError: if the xmsg_data_object is not an xMsgData instance
        """
        if isinstance(xmsg_data_object, xMsgData_pb2.xMsgData):
            return cls(topic, xmsg_data_object.SerializeToString())
        else:
            raise TypeError("xMsgMessage: Invalid type of data object")

    @classmethod
    def create_with_serialized_data(cls, topic, serialized_data):
        """
        Constructs a message with serialized data and the default metadata

        Args:
            topic (xMsgTopic): the topic of the message

            serialized (bytes): serialized data object

        Returns:
            xMsgMessage: xMsg message object
        """
        return cls(topic, serialized_data)

    def get_data(self):
        """
        Returns the message data

        Returns:
            bytes: data field as python bytes
        """
        return self.data

    def get_data_size(self):
        """Returns the size of the message data."""
        return sys.getsizeof(self.get_data())

    def set_data(self, serialized_data, mimetype):
        """
        Args:
            serialized_data (bytes[]): serialized data

            mimetype (string): mimetype for the data
        """
        self.data = serialized_data
        self.metadata.dataType = mimetype

    def get_metadata(self):
        """Returns metadata object (xMsgMeta)"""
        return self.metadata

    def get_metadata_bytes(self):
        """Returns metadata as python bytes"""
        return self.metadata.SerializeToString()

    def set_metadata(self, metadata):
        """
        Sets the metadata of this message.
        This will overwrite any mime-type already set.

        Args:
            metadata (xMsgMeta): the metadata for message
        """
        self.metadata.MergeFrom(metadata)

    def get_mimetype(self):
        """Returns the mime-type of the message data."""
        return self.metadata.dataType

    def set_mimetype(self, mimetype):
        """
        Sets the message mimetype

        Args:
            mimetype (string): data mimtype
        """
        self.metadata.dataType = mimetype

    def serialize(self):
        """
        Serializes this message into a ZMQ compatible message.

        Returns:
            Array: the ZMQ raw multi-part message
        """
        return [str(self.get_topic()), self.get_metadata_bytes(),
                self.get_data()]

    def get_topic(self):
        """Returns the topic string"""
        return self.topic
