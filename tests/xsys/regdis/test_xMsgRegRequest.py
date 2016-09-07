# coding=utf-8

import unittest

from xmsg.sys.regdis.xMsgRegRequest import xMsgRegRequest
from xmsg.core.xMsgExceptions import BadRequest
from xmsg.data.xMsgRegistration_pb2 import xMsgRegistration


class TestXMsgRegRequest(unittest.TestCase):

    def setUp(self):
        self.reg_info = xMsgRegistration()
        self.reg_info.host = "localhost"
        self.reg_info.name = "xMsgR"
        self.reg_info.subject = "test_subject"
        self.reg_info.domain = "domain"
        self.reg_info.type = "type_p"
        self.reg_info.port = 8888
        self.msg = ["topic", "sender", self.reg_info]
        self.serialized_msg = ["topic", "sender",
                               self.reg_info.SerializeToString()]

        self.req = xMsgRegRequest.create_from_multipart(self.msg)

    def test_constructor(self):
        self.assertIsInstance(self.req, xMsgRegRequest)

    def test_get_topic(self):
        self.assertEqual(self.req.topic, "topic")

    def test_get_sender(self):
        self.assertEqual(self.req.sender, "sender")

    def test_msg(self):
        self.assertEqual(self.req.msg(), self.serialized_msg)

    def test_raises_exception(self):
        bad_request_msg = ["topic", "sender"]

        with self.assertRaises(TypeError):
            xMsgRegRequest()
        with self.assertRaises(BadRequest):
            xMsgRegRequest.create_from_multipart(bad_request_msg)

if __name__ == "__main__":
    unittest.main()