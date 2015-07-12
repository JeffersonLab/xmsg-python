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
from xmsg.core.xMsgExceptions import TopicException, MessageException, RegistrationException


def broken_topic():
    raise TopicException("This is broken in topic")


def broken_message():
    raise MessageException("This is broken in message")


def broken_registration():
    raise RegistrationException("This is broken in registration")


class TestXMsgExceptions(unittest.TestCase):

    def testTopicExceptions(self):
        with self.assertRaises(TopicException) as context:
            broken_topic()
        self.assertTrue("This is broken in topic" in context.exception)

    def testMessageExceptions(self):
        with self.assertRaises(MessageException) as context:
            broken_message()
        self.assertTrue("This is broken in message" in context.exception)

    def testRegistrationExceptions(self):
        with self.assertRaises(RegistrationException) as context:
            broken_registration()
        self.assertTrue("This is broken in registration" in context.exception)
