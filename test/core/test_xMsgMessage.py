'''
Created on 02-06-2015

@author: royarzun
'''
import unittest
from core.xMsgMessage import xMsgMessage
from core.xMsgTopic import xMsgTopic
from data import xMsgMeta_pb2, xMsgData_pb2


class TestXMsgMessage(unittest.TestCase):

    def setUp(self):
        self.topic = xMsgTopic.wrap("a:b:c")
        self.message = xMsgMessage.create_with_serialized_data(self.topic,
                                                               bytes([1, 2, 3]))

    def test_get_topic(self):
        self.assertEqual("a:b:c", str(self.message.get_topic()))

    def test_set_serialize_data(self):
        msg = xMsgMessage.create_with_serialized_data(self.topic,
                                                      bytes([1, 2, 3]))
        self.assertEqual("a:b:c", str(self.message.get_topic()))
        self.assertEqual(msg.get_data(), bytes([1, 2, 3]))
        self.assertIsInstance(msg, xMsgMessage)

    def test_set_xmsg_data(self):
        data = xMsgData_pb2.xMsgData()
        data.type = xMsgData_pb2.xMsgData.T_FLSINT32A
        data.FLSINT32A.append(1)
        data.FLSINT32A.append(2)
        data.FLSINT32A.append(3)
        msg = xMsgMessage.create_with_xmsg_data(self.topic, data)
        self.assertEqual("a:b:c", str(self.message.get_topic()))
        ds_data = xMsgData_pb2.xMsgData()
        ds_data.ParseFromString(msg.get_data())
        self.assertEqual(data, ds_data)
        self.assertEqual(data.T_FLSINT32A, ds_data.T_FLSINT32A)
        self.assertIsInstance(msg, xMsgMessage)

    def test_msg(self):
        self.message.set_metadata(xMsgMeta_pb2.xMsgMeta())
        for data in self.message.msg():
            self.assertIsInstance(data, basestring)

    def test_set_metadata(self):
        metadata = xMsgMeta_pb2.xMsgMeta()
        self.message.set_metadata(metadata)
        self.assertIsInstance(self.message.get_metadata(),
                              xMsgMeta_pb2.xMsgMeta)

    def test_get_metadata(self):
        data = xMsgMeta_pb2.xMsgMeta()
        self.message.set_metadata(data)
        test_case = self.message.get_metadata()
        self.assertIsInstance(test_case, xMsgMeta_pb2.xMsgMeta)

if __name__ == "__main__":
    unittest.main()
