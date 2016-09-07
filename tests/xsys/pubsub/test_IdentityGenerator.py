# coding=utf-8

import unittest

from xmsg.sys.pubsub.IdentityGenerator import IdentityGenerator


class TestIdentityGenerator(unittest.TestCase):

    def test_ctrlId_has_nine_digits(self):
        self.assertEqual(9, len(str(IdentityGenerator.get_ctrl_id())))
        self.assertEqual(9, len(str(IdentityGenerator.get_ctrl_id())))
        self.assertEqual(9, len(str(IdentityGenerator.get_ctrl_id())))

    def test_ctr_id_prefix_has_three_digits(self):
        prefix1 = str(IdentityGenerator.get_ctrl_id())[1:4]
        prefix2 = str(IdentityGenerator.get_ctrl_id())[1:4]
        prefix3 = str(IdentityGenerator.get_ctrl_id())[1:4]

        self.assertEqual(prefix1, prefix2)
        self.assertEqual(prefix1, prefix3)
        self.assertEqual(prefix3, prefix2)

    def test_ctrl_id_first_digit_is_python_identifier(self):
        self.assertEqual('3', str(IdentityGenerator.get_ctrl_id())[0])
        self.assertEqual('3', str(IdentityGenerator.get_ctrl_id())[0])
        self.assertEqual('3', str(IdentityGenerator.get_ctrl_id())[0])

    def test_last_five_digits_are_random(self):
        self.assertNotEqual(IdentityGenerator.get_ctrl_id(),
                            IdentityGenerator.get_ctrl_id())
        self.assertNotEqual(IdentityGenerator.get_ctrl_id(),
                            IdentityGenerator.get_ctrl_id())
        self.assertNotEqual(IdentityGenerator.get_ctrl_id(),
                            IdentityGenerator.get_ctrl_id())


if __name__ == "__main__":
    unittest.main()
