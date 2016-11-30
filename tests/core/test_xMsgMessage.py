# coding=utf-8


import unittest

from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data.xMsgData_pb2 import xMsgData
from xmsg.data.xMsgMeta_pb2 import xMsgMeta


class TestXMsgMessage(unittest.TestCase):

    def setUp(self):
        self.topic = xMsgTopic.wrap("a:b:c")
        self.message = xMsgMessage(self.topic, bytes([1, 2, 3]))

    def test_get_topic(self):
        self.assertEqual("a:b:c", self.message.topic)

    def test_set_serialize_data(self):
        msg = xMsgMessage(self.topic, bytes([1, 2, 3]))
        self.assertEqual("a:b:c", self.message.topic)
        self.assertEqual(msg.data, bytes([1, 2, 3]))
        self.assertIsInstance(msg, xMsgMessage)

    def test_set_xmsg_data(self):
        data = xMsgData()
        data.type = xMsgData.T_FLSINT32A
        data.FLSINT32A.append(1)
        data.FLSINT32A.append(2)
        data.FLSINT32A.append(3)
        msg = xMsgMessage.from_xmsg_data(self.topic, data)
        self.assertEqual("a:b:c", self.message.topic)
        ds_data = xMsgData()
        ds_data.ParseFromString(msg.data)
        self.assertEqual(data, ds_data)
        self.assertEqual(data.T_FLSINT32A, ds_data.T_FLSINT32A)
        self.assertIsInstance(msg, xMsgMessage)

    def test_set_metadata(self):
        metadata = xMsgMeta()
        self.message.metadata = metadata
        self.assertIsInstance(self.message.metadata, xMsgMeta)

    def test_get_metadata_set_by_set_function(self):
        data = xMsgMeta()
        self.message.metadata = data
        test_case = self.message.metadata
        self.assertIsInstance(test_case, xMsgMeta)

    def test_get_metadata_set_by_default(self):
        test_case = self.message.metadata
        self.assertIsInstance(test_case, xMsgMeta)

if __name__ == "__main__":
    unittest.main()
