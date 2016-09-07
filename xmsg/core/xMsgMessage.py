# coding=utf-8

from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data.xMsgData_pb2 import xMsgData
from xmsg.data.xMsgMeta_pb2 import xMsgMeta


class xMsgMessage(object):
    """Defines a message to be serialized and passed through 0MQ.

    Uses xMsgData class generated as a result of the proto-buffer
    description to pass Python primitive types and arrays of primitive types.
    xMsgData is also used to pass bytes[]: the result of a user specific
    object serialization.

    This class also contains complete metadata of the message data,
    describing details of the data. In case an object is constructed
    without a metadata, the default metadata will be created and the
    proper data type will set based on the passed data parameter type.

    Attributes:
        topic (xMsgTopic): topic of the message
        metadata (xMsgMeta): metadata of the message
        data (bytes[]): serialized data object
    """

    def __init__(self, topic=None, serialized_data=None):
        # topic get stored as a basestring in case of xMsgTopic object str()
        # will convert it
        self._topic = str(topic)

        if(isinstance(serialized_data, basestring) or
           isinstance(serialized_data, bytearray) or
           isinstance(serialized_data, bytes) or
           isinstance(serialized_data, basestring)):
            self._data = serialized_data
            self._metadata = xMsgMeta()

        elif not serialized_data:
            self._metadata = xMsgMeta()

    @classmethod
    def create_with_string(cls, topic, data_string):
        """Constructs a message object with simple string data"""
        msg = cls()
        msg.topic = topic
        msg.data = data_string
        msg.mimetype = u"text/string"
        return msg

    @classmethod
    def create_with_xmsg_data(cls, topic, xmsg_data_object):
        """Constructs a message with an unserialized xMsgData object and
        the default metadata

        Args:
            topic (xMsgTopic): the topic of the message
            xmsg_data_object (xMsgData): the xMsgData object unserialized

        Returns:
            xMsgMessage: xMsg message object

        Raises:
            TypeError: if the xmsg_data_object is not an xMsgData instance
        """
        if isinstance(xmsg_data_object, xMsgData):
            msg = cls(topic, xmsg_data_object.SerializeToString())
            msg.metadata.dataType = u"binary/array-float"
            return msg
        else:
            raise TypeError("xMsgMessage: Invalid type of data object")

    @classmethod
    def create_with_serialized_data(cls, serialized_data):
        """Constructs a message with serialized data and the default metadata

        Args:
            serialized_data (bytes): serialized data object

        Returns:
            xMsgMessage: xMsg message object
        """
        msg = xMsgMessage()

        try:
            msg.topic = serialized_data[0]
            metadata = xMsgMeta()
            metadata.ParseFromString(serialized_data[1])
            msg.metadata = metadata
            msg.data = serialized_data[2]
            return msg

        except IndexError as index_error:
            raise Exception("xMsgMessage : %s" % index_error)

    @staticmethod
    def create_response(cls, msg):
        return cls(msg.get_reply_topic(), msg.metadata, msg.data)

    def has_reply_topic(self):
        return self._metadata.HasField("replyTo")

    def get_mimetype(self):
        return self._metadata.dataType

    def get_reply_topic(self):
        return xMsgTopic.wrap(self._metadata.replyTo)

    @property
    def data(self):
        """Returns the message data

        Returns:
            bytes: data field as python bytes
        """
        return self._data

    @data.setter
    def data(self, serialized_data):
        """Sets the serialized data and the mimetype for the message

        Args:
            serialized_data (bytes[]): serialized data
        """
        self._data = serialized_data

    @property
    def metadata(self):
        """Returns metadata object (xMsgMeta)

        Returns:
            xMsgMeta: message metadata object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this message.

        This will overwrite any mime-type already set.

        Args:
            metadata (xMsgMeta): the metadata for message
        """
        self._metadata.MergeFrom(metadata)

    @property
    def mimetype(self):
        """Returns the mime-type of the message data.

        Returns:
            String: mimetype for message data
        """
        return self._metadata.dataType

    @mimetype.setter
    def mimetype(self, mimetype):
        """Sets the message mimetype

        Args:
            mimetype (String): data mimetype
        """
        self._metadata.dataType = mimetype

    @property
    def topic(self):
        """Returns the topic string

        Returns:
            String: message topic
        """
        return str(self._topic)

    @topic.setter
    def topic(self, topic):
        """Sets the topic for xMsgMessage instance

        Args:
            topic (String): message
        """
        self._topic = topic

    def serialize(self):
        """Serializes this message into a ZMQ compatible message.

        Returns:
            list: the ZMQ raw multi-part message
        """
        return [self._topic, self._metadata.SerializeToString(), self._data]
