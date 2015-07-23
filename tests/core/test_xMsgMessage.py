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
import unittest

from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data import xMsgMeta_pb2, xMsgData_pb2


class TestXMsgMessage(unittest.TestCase):

    def setUp(self):
        self.topic = xMsgTopic.wrap("a:b:c")
        self.message = xMsgMessage.create_with_serialized_data(self.topic,
                                                               bytes([1, 2, 3]))

    def test_get_topic(self):
        self.assertEqual("a:b:c", str(self.message.get_topic()))

    def test_get_topic_object(self):
        self.assertIsInstance(self.message.get_topic(), xMsgTopic)

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

    def test_serialize(self):
        self.message.set_metadata(xMsgMeta_pb2.xMsgMeta())
        for data in self.message.serialize():
            self.assertIsInstance(data, basestring)

    def test_set_metadata(self):
        metadata = xMsgMeta_pb2.xMsgMeta()
        self.message.set_metadata(metadata)
        self.assertIsInstance(self.message.get_metadata(),
                              xMsgMeta_pb2.xMsgMeta)

    def test_get_metadata_bytes(self):
        self.assertIsInstance(self.message.get_metadata_bytes(),
                              basestring)

    def test_get_metadata_set_by_set_function(self):
        data = xMsgMeta_pb2.xMsgMeta()
        self.message.set_metadata(data)
        test_case = self.message.get_metadata()
        self.assertIsInstance(test_case, xMsgMeta_pb2.xMsgMeta)

    def test_get_metadata_set_by_default(self):
        test_case = self.message.get_metadata()
        self.assertIsInstance(test_case, xMsgMeta_pb2.xMsgMeta)

if __name__ == "__main__":
    unittest.main()
