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
            data.STRING = data_object
        elif isinstance(data_object, int):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT32
            data.FLSINT32 = data_object
        elif isinstance(data_object, long):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT64
            data.FLSINT64 = data_object
        elif isinstance(data_object, float):
            data.type = xMsgData_pb2.xMsgData.T_FLOAT
            data.FLOAT = data_object
        elif all(isinstance(item, int) for item in data_object):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT32A
            for i in data_object:
                data.FLSINT32A.append(int(i))
        elif all(isinstance(item, long) for item in data_object):
            data.type = xMsgData_pb2.xMsgData.T_FLSINT64A
            for i in data_object:
                data.FLSINT64A.append(long(i))
        elif all(isinstance(item, long) for item in data_object):
            data.type = xMsgData_pb2.xMsgData.T_FLOATA
            for i in data_object:
                data.FLOATA.append(float(i))
        self.data = data

    def get_metadata_bytes(self):
        return self.metadata.SerializeToString()

    def get_data_bytes(self):
        return self.data.SerializeToString()
