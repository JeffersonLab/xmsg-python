'''
Created on 02-06-2015

@author: royarzun
'''
import unittest
from core.xMsgMessage import xMsgMessage
from data import xMsgMeta_pb2


class TestXMsgMessage(unittest.TestCase):

    def setUp(self):
        self.message = xMsgMessage("a:b:c")

    def test_get_topic(self):
        self.assertEqual("a:b:c", self.message.get_topic())

    def test_set_topic(self):
        self.message.set_topic("d:e:f")
        self.assertEqual("d:e:f", self.message.get_topic())

    def test_set_metadata(self):
        data = xMsgMeta_pb2.xMsgMeta()
        self.message.set_metadata(data)
        self.assertIsInstance(self.message.get_metadata(),
                              xMsgMeta_pb2.xMsgMeta)

    def test_get_metadata(self):
        data = xMsgMeta_pb2.xMsgMeta()
        self.message.set_metadata(data)
        test_case = self.message.get_metadata()
        self.assertIsInstance(test_case, xMsgMeta_pb2.xMsgMeta)

if __name__ == "__main__":
    unittest.main()