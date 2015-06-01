'''
Created on 28-05-2015

@author: royarzun
'''
import unittest
import mock
import zmq

from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from xsys.regdis.xMsgRegistrar import xMsgRegistrar


class TestXMsgRegistrar(unittest.TestCase):

    @mock.patch('data.xMsgRegistrationData_pb2.xMsgRegistrationData')
    def setUp(self, reg_data):
        self.registrar = xMsgRegistrar(zmq.Context)
        self.data = reg_data()

    def test_get_registration(self):
        pass
    
    def test__reply_success(self):
        topic = "xxxx:yyyy:zzzz"
        subject = str(xMsgUtil.get_local_ip()) + \
                  ":" + str(xMsgConstants.REGISTRAR)
        test_case = self.registrar._reply_success(topic)
        self.assertEqual(test_case, [topic,
                                     subject,
                                     str(xMsgConstants.SUCCESS)])
    def test__reply_message(self):
        topic = "xxxx:yyyy:zzzz"
        subject = str(xMsgUtil.get_local_ip()) + \
                  ":" + str(xMsgConstants.REGISTRAR)
        test_case = self.registrar._reply_success(topic)
        self.assertEqual(test_case, [topic,
                                     subject,
                                     str(xMsgConstants.SUCCESS)])
        
    def test__get_key(self):
        self.data.domain = "somedomain"
        self.data.subject = str(xMsgConstants.UNDEFINED)
        self.data.xtype = str(xMsgConstants.UNDEFINED)
        test_case = self.registrar._get_key(self.data)
        self.assertEqual(test_case, "somedomain")
        self.data.subject = "somesubject"
        test_case = self.registrar._get_key(self.data)
        self.assertEqual(test_case, "somedomain:somesubject")
        self.data.xtype = "sometype"
        test_case = self.registrar._get_key(self.data)
        self.assertEqual(test_case, "somedomain:somesubject:sometype")
    

if __name__ == "__main__":
    unittest.main()
