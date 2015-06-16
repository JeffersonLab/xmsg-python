'''
Created on 22-05-2015

@author: royarzun
'''
import unittest
from core.xMsgUtil import xMsgUtil
from core.xMsgExceptions import MalformedCanonicalName, UndefinedTopicDomain
from core.xMsgConstants import xMsgConstants

VALID_CASES = ["aaaa:bbbb:cccc",
               "aa_a:bb_b:cc_c",
               "_aaa:_bbb:_ccc",
               "aaaa:bbbb",
               ]

INVALID_CASES = [" aaa:bbbb:cccc",
                 "aaaa::bbbb::cccc",
                 " aaa: bbb: ccc",
                 " aaa: bbb",
                 "aaa :bbb ",
                 ]

VALID_TYPE_CASES = ["aaaa:bbbb:cccc",
                    "aa_a:bb_b:cc_c",
                    "_aaa:_bbb:_ccc",
                    ]

INVALID_TYPE_CASES = [" aaa:bbbb:cccc",
                      "aaaa::bbbb::cccc",
                      " aaa: bbb: ccc",
                      ]

BUILD_TOPIC_CASES = [{"args": {"domain": "d", "subject" : "s", "xtype": "t"},
                      "result": "d:s:t"},
                     {"args": {"domain": "d", "subject" : "s"},
                      "result": "d:s"},
                     {"args": {"domain": "d"},
                      "result": "d"},
                     {"args": {"domain": "d", "subject" : "*"},
                      "result": "d"},
                     {"args": {"domain": "d", "subject" : "s", "xtype" : "*"},
                      "result": "d:s"},
                     ]

class TestXMsgUtil(unittest.TestCase):

    def setUp(self):
        pass

    def test_build_topic(self):
        for case in BUILD_TOPIC_CASES:
            test_case = xMsgUtil.build_topic(**case["args"])
            self.assertEqual(test_case, case["result"])

    def test_build_topic_raises_exception(self):
        self.assertRaises(UndefinedTopicDomain,
                          xMsgUtil.build_topic, None, "s", "t")
        self.assertRaises(UndefinedTopicDomain,
                          xMsgUtil.build_topic, "*", "s", "t")

    def test_get_domain(self):
        for case in VALID_CASES:
            test_case = xMsgUtil.get_domain(case)
            self.assertIsNotNone(test_case)
        for case in INVALID_CASES:
            self.assertRaises(MalformedCanonicalName,
                              xMsgUtil.get_domain, case)

    def test_get_subject(self):
        for case in VALID_CASES:
            test_case = xMsgUtil.get_subject(case)
            self.assertIsNotNone(test_case)
        for case in INVALID_CASES:
            self.assertRaises(MalformedCanonicalName,
                              xMsgUtil.get_subject, case)

    def test_get_type(self):
        for case in VALID_TYPE_CASES:
            test_case = xMsgUtil.get_type(case)
            self.assertIsNotNone(test_case)
        for case in INVALID_TYPE_CASES:
            self.assertRaises(MalformedCanonicalName,
                              xMsgUtil.get_type, case)
            
    def test_get_local_ip(self):
        test_case = xMsgUtil.get_local_ip()
        self.assertIsInstance(test_case, basestring)

if __name__ == "__main__":
    unittest.main()
