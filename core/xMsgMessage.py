from core.xMsgConstants import xMsgConstants
from data import xMsgMeta_pb2
from data import xMsgData_pb2

__author__ = 'gurjyan'


class xMsgMessage():
    topic = str(xMsgConstants.UNDEFINED)
    metadata = str(xMsgConstants.UNDEFINED)
    data = str(xMsgConstants.UNDEFINED)

    def __init__(self, topic, metadata=None, data=None):
        self.topic = topic
        self.metadata = metadata
        self.data = data

    def get_topic(self):
        return self.topic

    def set_topic(self, topic):
        self.topic = topic

    def get_metadata(self):
        return self.metadata

    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_data(self):
        return self.data

    def set_data(self, data_object):
        metadata = xMsgMeta_pb2.xMsgMeta()
        metadata.dataType = xMsgMeta_pb2.xMsgMeta.X_Object
        self.metadata = metadata
        data = xMsgData_pb2.xMsgData()

        if isinstance(data_object, basestring):
            data.type = xMsgData_pb2.xMsgData.T_STRING
        elif isinstance(data_object, int):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT32
            data.FLSINT32 = data_object
        elif isinstance(data_object, long):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT64
            data.T_FLSINT64 = data_object
        elif isinstance(data_object, float):
            data.type = xMsgData_pb2.xMsgData.T_FLOAT
            data.FLOAT = data_object
        elif isinstance(data_object, int):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT32A
            data.FLSINT32A = data_object
        self.data = data

    def get_metadata_bytes(self):
        return self.metadata.SerializeToString()

    def get_data_bytes(self):
        return self.data.SerializeToString()
