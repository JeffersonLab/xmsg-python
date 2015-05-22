'''
Created on 22-05-2015

@author: royarzun
'''
import unittest
from core.xMsgUtil import xMsgUtil

VALID_CASES = ["aaaa:bbbb:cccc",
               "aa_a:bb_b:cc_c",
               "_aaa:_bbb:_ccc",
               "aaaa:bbbb",
               "aaaa",
               ]

INVALID_CASES = [" aaa:bbbb:cccc",
                 "aaaa::bbbb::cccc",
                 " aaa: bbb: ccc",
                 " aaa: bbb",
                 "aaa :bbb ",
                 ]


class TestXMsgUtil(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_domain_positive(self):
        for case in VALID_CASES:
            test_case = xMsgUtil.get_domain(case)
            self.assertIsNotNone(test_case)

    def test_get_domain_negative(self):
        for case in INVALID_CASES:
            self.assertRaises(Exception, xMsgUtil.get_domain, case)

    def get_subject_positive(self):
        for case in VALID_CASES:
            test_case = xMsgUtil.get_subject(case)
            self.assertIsNotNone(test_case)

    def get_subject_negative(self):
        for case in INVALID_CASES:
            self.assertRaises(Exception, xMsgUtil.get_subject, case)

if __name__ == "__main__":
    unittest.main()
