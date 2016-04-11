# coding=utf-8

import unittest

from xmsg.core.xMsgExceptions import UndefinedTopicDomain
from xmsg.core.xMsgTopic import xMsgTopic

VALID_CASES = ["aaaa:bbbb:cccc",
               "aa_a:bb_b:cc_c",
               "_aaa:_bbb:_ccc"]


BUILD_TOPIC_CASES = [{
                      "args": {
                               "domain": "d",
                               "subject": "s",
                               "xtype": "t"
                               },
                      "result": "d:s:t"
                      },
                     {"args": {
                               "domain": "_ddd",
                               "subject": "sss_s",
                               "xtype": "t_ttt"
                               },
                      "result": "_ddd:sss_s:t_ttt"
                      }]


class TestXMsgTopic(unittest.TestCase):

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

    def test_is_parent_method(self):
        topic_parent = xMsgTopic.wrap("domain:subject")
        topic = xMsgTopic.wrap("domain:subject:type1")
        self.assertTrue(topic_parent.is_parent(topic))


if __name__ == "__main__":
    unittest.main()
