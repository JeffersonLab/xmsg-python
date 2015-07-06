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

from xsys.regdis.xMsgRegRequest import xMsgRegRequest
from core.xMsgExceptions import BadRequest
from data import xMsgRegistration_pb2


class TestXMsgRegRequest(unittest.TestCase):

    def setUp(self):
        self.reg_info = xMsgRegistration_pb2.xMsgRegistration()
        self.reg_info.host = "localhost"
        self.reg_info.name = "xMsgR"
        self.reg_info.subject = "test_subject"
        self.reg_info.domain = "domain"
        self.reg_info.type = "type_p"
        self.reg_info.port = 8888
        self.msg = ["topic", "sender", self.reg_info.SerializeToString()]

        self.req = xMsgRegRequest.create_from_multipart_request(self.msg)

    def test_constructor(self):
        self.assertIsInstance(self.req, xMsgRegRequest)

    def test_get_topic(self):
        self.assertEqual(self.req.get_topic(), "topic")

    def test_get_sender(self):
        self.assertEqual(self.req.get_sender(), "sender")

    def test_msg(self):
        self.assertEqual(self.req.get_serialized_msg(), self.msg)

    def test_get_data(self):
        self.assertIsInstance(self.req.get_data(),
                              xMsgRegistration_pb2.xMsgRegistration)

    def test_raises_exception(self):
        bad_request_msg = ["topic", "sender"]
        test_case = xMsgRegRequest()
        with self.assertRaises(BadRequest):
            test_case.create_from_multipart_request(bad_request_msg)

if __name__ == "__main__":
    unittest.main()