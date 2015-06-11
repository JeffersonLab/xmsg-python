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
from xsys.regdis.xMsgRegRequest import xMsgRegRequest


class TestXMsgRegRequest(unittest.TestCase):

    def setUp(self):
        self.msg = ["topic", "sender", "data"]
        self.req = xMsgRegRequest(self.msg)

    def test_constructor(self):
        self.assertIsInstance(self.req, xMsgRegRequest)

    def test_get_topic(self):
        self.assertEqual(self.req.get_topic(), "topic")

    def test_get_sender(self):
        self.assertEqual(self.req.get_sender(), "sender")

    def test_msg(self):
        self.assertEqual(self.req.get_msg(), self.msg)

if __name__ == "__main__":
    unittest.main()