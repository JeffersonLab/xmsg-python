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
from xsys.regdis.xMsgRegDatabase import xMsgRegDatabase
from data import xMsgRegistration_pb2
from sets import Set


class TestXMsgRegDatabase(unittest.TestCase):

    def setUp(self):
        self.db = xMsgRegDatabase()
        self.reg_info = xMsgRegistration_pb2.xMsgRegistration()
        self.reg_info.domain = "test_domain"
        self.reg_info.subject = "test_subject"
        self.reg_info.type = "test_type"
        self.reg_info.name = "test_name"
        self.reg_info.description = "some test description..."
        self.reg_info.host = "localhost"
        self.reg_info.port = 8000

        self.topic = "test_domain:test_subject:test_type"
        self.undefined_topic = "test_domain:test_subject:test_typexxx"

    def test_register(self):
        self.db.register(self.reg_info)
        self.assertEqual(self.db.get(self.topic),
                         Set([self.reg_info.SerializeToString()]))

    def test_get_some_result(self):
        self.db.register(self.reg_info)
        self.assertIsNotNone(self.db.get(self.topic))

    def test_get_none_result(self):
        self.db.register(self.reg_info)
        self.assertIsNone(self.db.get(self.undefined_topic))

    def test_remove(self):
        self.db.register(self.reg_info)
        self.db.remove(self.reg_info)
        self.assertIsNone(self.db.get(self.topic))

    def test_remove_by_host(self):
        self.db.register(self.reg_info)
        self.db.remove_by_host("localhost")
        self.assertIsNone(self.db.get(self.topic))

    def test_get_all_publishers_in_domain(self):
        set_all = Set([self.reg_info.SerializeToString()])
        self.db.register(self.reg_info)
        test_case = self.db.find("test_domain", "*", "*")
        self.assertEqual(test_case, set_all)

    def test_topic(self):
        set_topic = Set([self.reg_info.SerializeToString()])
        self.db.register(self.reg_info)
        self.assertEqual(self.db.get(self.topic), set_topic)

    def test_topic_none(self):
        self.assertIsNone(self.db.get(self.undefined_topic))

if __name__ == "__main__":
    unittest.main()
