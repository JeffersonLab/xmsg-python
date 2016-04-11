# coding=utf-8

import unittest

from xmsg.core.xMsgUtil import xMsgUtil as utils
from xmsg.data import xMsgRegistration_pb2

IPREGX = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}" + \
         "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"


class TestXMsgUtil(unittest.TestCase):

    def test_build_registration(self):
        register = utils.build_registration("some name",
                                            "some description",
                                            "some domain",
                                            "some subject",
                                            "some type",
                                            True)
        self.assertIsInstance(register,
                              xMsgRegistration_pb2.xMsgRegistration)

    def test_get_local_ip(self):
        test_case = utils.get_local_ip()
        self.assertIsInstance(test_case, basestring)

    def test_get_local_ips(self):
        test_case = utils.get_local_ips()
        self.assertIsNot(len(test_case), 0)
        for ip in test_case:
            self.assertRegexpMatches(str(ip), IPREGX)
            self.assertEqual(True, utils.is_ip(ip))

if __name__ == "__main__":
    unittest.main()
