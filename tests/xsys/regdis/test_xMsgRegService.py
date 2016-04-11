# coding=utf-8

import unittest
import zmq

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.xsys.regdis.xMsgRegService import xMsgRegService
from xmsg.net.xMsgAddress import RegAddress


class TestXMsgRegService(unittest.TestCase):
    reg_info = xMsgUtil.build_registration("test_name", "test_description",
                                           "test_domain", "test_subject",
                                           "test_type", True)
    sender = "test_sender"

    def setUp(self):
        context = zmq.Context()
        self.reg_serv = xMsgRegService(context, RegAddress())

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
