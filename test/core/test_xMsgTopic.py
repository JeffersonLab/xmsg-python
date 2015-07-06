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
from core.xMsgExceptions import UndefinedTopicDomain
from core.xMsgTopic import xMsgTopic

VALID_CASES = ["aaaa:bbbb:cccc",
               "aa_a:bb_b:cc_c",
               "_aaa:_bbb:_ccc",
               ]


BUILD_TOPIC_CASES = [{"args": {"domain": "d", "subject" : "s", "xtype": "t"},
                      "result": "d:s:t"},
                     {"args": {"domain": "_ddd", "subject" : "sss_s", "xtype": "t_ttt"},
                      "result": "_ddd:sss_s:t_ttt"},
                     ]


class TestXMsgTopic(unittest.TestCase):

    def setUp(self):
        pass

    def test_build_topic(self):
        for case in BUILD_TOPIC_CASES:
            test_case = xMsgTopic.build(**case["args"])
            self.assertEqual(str(test_case), case["result"])

    def test_build_topic_raises_exception(self):
        self.assertRaises(UndefinedTopicDomain,
                          xMsgTopic.build, None, "s", "t")
        self.assertRaises(UndefinedTopicDomain,
                          xMsgTopic.build, "*", "s", "t")

    def test_get_domain(self):
        for case in BUILD_TOPIC_CASES:
            test_case = xMsgTopic.build(**case["args"])
            self.assertIsNotNone(test_case.domain())

    def test_get_subject(self):
        for case in BUILD_TOPIC_CASES:
            test_case = xMsgTopic.build(**case["args"])
            self.assertIsNotNone(test_case.subject())

    def test_get_type(self):
        for case in BUILD_TOPIC_CASES:
            test_case = xMsgTopic.build(**case["args"])
            self.assertIsNotNone(test_case.type())

    def test_wrap_builder(self):
        for case in VALID_CASES:
            test_case = xMsgTopic.wrap(case)
            self.assertIsInstance(test_case, xMsgTopic)
            validated = str(test_case) in VALID_CASES
            self.assertEqual(validated, True)
