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
from xsys.regdis.xMsgRegistrationService import xMsgRegistrationService


class TestXMsgRegistrationService(unittest.TestCase):

    def setUp(self):
        self.r_service = xMsgRegistrationService(zmq.Context)
        self.topic0 = "domain:subject_p:type_p"
        self.topic1 = "domain:subject_s:type_s"
        self.r_service._register(self.topic0, "data_p1", True)
        self.r_service._register(self.topic0, "data_p2", True)
        self.r_service._register(self.topic1, "data_s1", False)
        self.r_service._register(self.topic1, "data_s2", False)

    def test_get_registration_publisher(self):
        set_pubs = Set(["data_p1", "data_p2"])
        test_case = self.r_service._get_registration_new("domain",
                                                         "subject_p",
                                                         "type_p", True)
        self.assertEqual(test_case[0].issubset(set_pubs), True)

    def test_get_registration_subscriber(self):
        set_subs = Set(["data_s1", "data_s2"])
        test_case = self.r_service._get_registration_new("domain",
                                                         "subject_s",
                                                         "type_s",
                                                         False)
        self.assertEqual(test_case[0].issubset(set_subs), True)

    def test_get_all_publishers_in_domain(self):
        set_all = Set(["data_p1", "data_p2", "data_s1", "data_s2"])
        test_case = self.r_service._get_registration_new("domain",
                                                         "*",
                                                         "*", True)
        print self.r_service.publishers_db
        self.assertEqual(test_case[0].issubset(set_all), True)

if __name__ == "__main__":
    unittest.main()
