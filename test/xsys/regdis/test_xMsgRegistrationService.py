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
from data import xMsgRegistration_pb2
from xsys.regdis.xMsgRegDatabase import xMsgRegDatabase


class TestXMsgRegistrationService(unittest.TestCase):

    def setUp(self):
        self.db = xMsgRegDatabase()

        self.topic = "domain:test_subject:type_p"

        self.reg_info = xMsgRegistration_pb2.xMsgRegistration()
        self.reg_info.host = "localhost"
        self.reg_info.name = "xMsgR"
        self.reg_info.subject = "test_subject"
        self.reg_info.domain = "domain"
        self.reg_info.type = "type_p"
        self.reg_info.port = 8888

if __name__ == "__main__":
    unittest.main()
