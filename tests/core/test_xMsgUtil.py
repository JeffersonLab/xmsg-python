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

from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data import xMsgRegistration_pb2

IPREGX = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}"+\
         "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"


class TestXMsgUtil(unittest.TestCase):

    def setUp(self):
        pass

    def test_build_registration(self):
        register = xMsgUtil.build_registration("somename",
                                               "somedesc",
                                               "somedomain",
                                               "somesubject",
                                               "sometype",
                                               True)
        self.assertIsInstance(register,
                              xMsgRegistration_pb2.xMsgRegistration) 
            
    def test_get_local_ip(self):
        test_case = xMsgUtil.get_local_ip()
        self.assertIsInstance(test_case, basestring)

    def test_get_local_ips(self):
        test_case = xMsgUtil.get_local_ips()
        self.assertIsNot(len(test_case), 0)
        for ip in test_case:
            self.assertRegexpMatches(str(ip), IPREGX)
            self.assertEqual(True, xMsgUtil.is_ip(ip))

if __name__ == "__main__":
    unittest.main()
