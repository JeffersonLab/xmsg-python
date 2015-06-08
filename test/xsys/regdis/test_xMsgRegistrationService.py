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
from sets import Set
import unittest
import zmq
from data import xMsgRegistration_pb2
from xsys.regdis.xMsgRegistrationService import xMsgRegistrationService


class TestXMsgRegistrationService(unittest.TestCase):

    def setUp(self):
        self.reg_info = xMsgRegistration_pb2.xMsgRegistration()
        self.reg_info.host = "localhost"
        self.reg_info.name = "xMsgR"
        self.reg_info.subject = "test_subject"
        self.reg_info.domain = "domain"
        self.reg_info.type = "type_p"
        self.reg_info.port = 8888

        self.r_service = xMsgRegistrationService(zmq.Context)
        self.topic0 = "domain:test_subject:type_p"
        self.topic1 = "domain:test_subject:type_s"
        self.r_service._register(self.topic0, self.reg_info, True)
        self.r_service._register(self.topic0, self.reg_info, True)
        self.r_service._register(self.topic1, self.reg_info, False)
        self.r_service._register(self.topic1, self.reg_info, False)

    def test_get_registration_publisher(self):
        set_pubs = Set(["data_p1", "data_p2"])
        test_case = self.r_service._get_registration_new("domain",
                                                         "subject",
                                                         "type_p", True)
        self.assertEqual(test_case.issubset(set_pubs), True)

    def test_get_registration_subscriber(self):
        set_subs = Set(["data_s1", "data_s2"])
        test_case = self.r_service._get_registration_new("domain",
                                                         "subject",
                                                         "type_s",
                                                         False)
        self.assertEqual(test_case.issubset(set_subs), True)

    def test_get_all_publishers_in_domain(self):
        set_all = Set([self.reg_info.SerializeToString()])
        test_case = self.r_service._get_registration_new("domain",
                                                         "*",
                                                         "*", True)
        self.assertEqual(set_all, test_case)

    def test__remove_register(self):

        self.r_service._remove_register("domain:test_subject:type_p",
                                        self.reg_info, True)
        self.r_service._remove_register("domain:test_subject:type_p",
                                        self.reg_info, True)
        self.r_service._remove_register("domain:test_subject:type_s",
                                        self.reg_info, False)
        self.r_service._remove_register("domain:test_subject:type_s",
                                        self.reg_info, False)
        self.assertEqual(self.r_service.publishers_db, {})
        self.assertEqual(self.r_service.subscribers_db, {})

if __name__ == "__main__":
    unittest.main()
