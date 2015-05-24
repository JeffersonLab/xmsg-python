'''
Created on 22-05-2015

@author: royarzun
'''
import unittest
from core.xMsgUtil import xMsgUtil
from core.xMsgExceptions import MalformedCanonicalName

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


class TestXMsgUtil(unittest.TestCase):

    def setUp(self):
        pass

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

if __name__ == "__main__":
    unittest.main()
