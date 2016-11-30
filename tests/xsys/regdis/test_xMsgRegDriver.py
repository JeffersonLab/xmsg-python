# coding=utf-8

import unittest
import zmq
from mockito import any, when, verify, spy

from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.net.xMsgAddress import RegAddress
from xmsg.sys.regdis.xMsgRegDriver import xMsgRegDriver
from xmsg.sys.regdis.xMsgRegRequest import xMsgRegRequest
from xmsg.sys.regdis.xMsgRegResponse import xMsgRegResponse


class TestxMsgRegDriver(unittest.TestCase):
    publisher = xMsgUtil.build_registration("bradbury_pub", "bradbury books",
                                            "writer", "scifi", "books", True)
    subscriber = xMsgUtil.build_registration("bradbury_sub",
                                             "bradbury description",
                                             "writer", "scifi", "books", False)

    def setUp(self):
        self.context = spy(zmq.Context())
        self.ln_connection = self.context.socket(zmq.REQ)

        self.driver = xMsgRegDriver(self.context, RegAddress("localhost"))
        self.set_response(xMsgRegResponse("", "", ""))

    def test_send_local_publisher_registration(self):
        self.driver.add(self.publisher, True)

        self.assert_request(self.ln_connection,
                            self.publisher,
                            xMsgConstants.REGISTER_PUBLISHER,
                            xMsgConstants.REGISTER_REQUEST_TIMEOUT)

    def test_send_local_subscriber_registration(self):
        self.driver.add(self.subscriber, False)

        self.assert_request(self.ln_connection,
                            self.subscriber,
                            xMsgConstants.REGISTER_SUBSCRIBER,
                            xMsgConstants.REGISTER_REQUEST_TIMEOUT)

    def test_send_local_publisher_removal(self):
        self.driver.remove(self.publisher, True)

        self.assert_request(self.ln_connection,
                            self.publisher,
                            xMsgConstants.REMOVE_PUBLISHER,
                            xMsgConstants.REMOVE_REQUEST_TIMEOUT)

    def test_send_local_subscriber_removal(self):
        self.driver.remove(self.subscriber, False)

        self.assert_request(self.ln_connection,
                            self.subscriber,
                            xMsgConstants.REMOVE_SUBSCRIBER,
                            xMsgConstants.REMOVE_REQUEST_TIMEOUT)

    def test_send_local_publisher_find(self):
        self.driver.find(self.publisher, True)

        self.assert_request(self.ln_connection,
                            self.publisher,
                            xMsgConstants.FIND_PUBLISHER,
                            xMsgConstants.FIND_REQUEST_TIMEOUT)

    def test_send_local_subscriber_find(self):
        self.driver.find(self.subscriber, False)

        self.assert_request(self.ln_connection,
                            self.subscriber,
                            xMsgConstants.FIND_SUBSCRIBER,
                            xMsgConstants.FIND_REQUEST_TIMEOUT)

    def test_remove_all(self):
        self.driver.remove_all("10.2.9.1")

        self.assert_remove_request(self.ln_connection,
                                   "self.subscriber",
                                   xMsgConstants.REMOVE_ALL_REGISTRATION,
                                   xMsgConstants.FIND_REQUEST_TIMEOUT)

    def assert_request(self, socket, data, topic, timeout):
        request_object = xMsgRegRequest(topic, data.name, data)

        self.driver.request(socket, request_object, timeout)
        verify(self.driver).request(socket, request_object, timeout)

    def assert_remove_request(self, socket, data, topic, timeout):
        request_object = xMsgRegRequest(topic, "reg_driver", data)

        self.driver.request(socket, request_object, timeout)
        verify(self.driver).request(socket, request_object, timeout)

    def set_response(self, response):
        when(self.driver).request(any(xMsgRegRequest),
                                  any(int)).thenReturn(response)

if __name__ == "__main__":
    unittest.main()
