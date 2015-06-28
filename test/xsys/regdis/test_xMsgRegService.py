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
import zmq

from core.xMsgConstants import xMsgConstants
from data import xMsgRegistration_pb2
from xsys.regdis.xMsgRegService import xMsgRegService


class TestXMsgRegService(unittest.TestCase):

    def setUp(self):
        self.reg_serv = xMsgRegService(zmq.Context())

        self.topic = "domain:test_subject:type_p"
        self.sender = "some_sender"

        self.reg_info = xMsgRegistration_pb2.xMsgRegistration()
        self.reg_info.host = "localhost"
        self.reg_info.name = "xMsgR"
        self.reg_info.subject = "test_subject"
        self.reg_info.domain = "domain"
        self.reg_info.type = "type_p"
        self.reg_info.port = 8888

    def test_register_publisher(self):
        request = [str(xMsgConstants.REGISTER_PUBLISHER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertEqual(test_case.get_status(), "success")

    def test_register_subscriber(self):
        request = [str(xMsgConstants.REGISTER_SUBSCRIBER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertEqual(test_case.get_status(), "success")

    def test_remove_publisher(self):
        request = [str(xMsgConstants.REMOVE_PUBLISHER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertEqual(test_case.get_status(), "success")

    def test_remove_subscriber(self):
        request = [str(xMsgConstants.REMOVE_SUBSCRIBER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertEqual(test_case.get_status(), "success")

    def test_remove_all_regs(self):
        request = [str(xMsgConstants.REMOVE_ALL_REGISTRATION),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertEqual(test_case.get_status(), "success")

    def test_find_publisher(self):
        request = [str(xMsgConstants.REGISTER_PUBLISHER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        self.reg_serv.process_request(request)
        request = [str(xMsgConstants.FIND_PUBLISHER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertIsNotNone(test_case.get_data())

    def test_find_subscriber(self):
        request = [str(xMsgConstants.REGISTER_SUBSCRIBER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        self.reg_serv.process_request(request)
        request = [str(xMsgConstants.FIND_SUBSCRIBER),
                   self.sender,
                   self.reg_info.SerializeToString()]
        test_case = self.reg_serv.process_request(request)
        self.assertIsNotNone(test_case.get_data())

if __name__ == "__main__":
    unittest.main()
