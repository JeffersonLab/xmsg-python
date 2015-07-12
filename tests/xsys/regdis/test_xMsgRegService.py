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

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.xsys.regdis.xMsgRegService import xMsgRegService


class TestXMsgRegService(unittest.TestCase):
    reg_info = xMsgUtil.build_registration("test_name", "test_description", "test_domain",
                                           "test_subject", "test_type", True)
    topic = "test_domain:test_subject:test_type"
    sender = "test_sender"

    def setUp(self):
        self.reg_serv = xMsgRegService(zmq.Context())

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
