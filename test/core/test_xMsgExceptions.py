'''
Created on 28-05-2015

@author: royarzun
'''
import unittest
from core.xMsgExceptions import TopicException, MessageException,\
                                RegistrationException


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
