#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
import unittest
import zmq
from mockito import any, when, verify, spy

from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver
from xmsg.xsys.regdis.xMsgRegRequest import xMsgRegRequest
from xmsg.xsys.regdis.xMsgRegResponse import xMsgRegResponse


class TestxMsgRegDriver(unittest.TestCase):
    publisher = xMsgUtil.build_registration("bradbury_pub", "bradbury books", "writer",
                                            "scifi", "books", True)
    subscriber = xMsgUtil.build_registration("bradbury_sub", "bradbury description", "writer",
                                             "scifi", "books", False)

    def setUp(self):
        self.context = spy(zmq.Context())
        self.ln_connection = self.context.socket(zmq.REQ)
        self.fe_connection = self.context.socket(zmq.REQ)

        self.driver = xMsgRegDriver(self.context)
        self.set_response(xMsgRegResponse("", "", ""))

    def test_send_local_publisher_registration(self):
        self.driver.register_local("bradbury_pub", self.publisher, True)

        self.assert_request(self.ln_connection,
                            "bradbury_pub",
                            self.publisher,
                            str(xMsgConstants.REGISTER_PUBLISHER),
                            str(xMsgConstants.REGISTER_REQUEST_TIMEOUT))

    def test_send_local_subscriber_registration(self):
        self.driver.register_local("bradbury_sub", self.subscriber, False)

        self.assert_request(self.ln_connection,
                            "bradbury_sub",
                            self.subscriber,
                            str(xMsgConstants.REGISTER_SUBSCRIBER),
                            str(xMsgConstants.REGISTER_REQUEST_TIMEOUT))

    def test_send_frontend_publisher_registration(self):
        self.driver.register_fe("bradbury_pub", self.publisher, True)

        self.assert_request(self.fe_connection,
                            "bradbury_pub",
                            self.publisher,
                            str(xMsgConstants.REGISTER_PUBLISHER),
                            str(xMsgConstants.REGISTER_REQUEST_TIMEOUT))

    def test_send_frontend_subscriber_registration(self):
        self.driver.register_fe("bradbury_sub", self.subscriber, False)

        self.assert_request(self.fe_connection,
                            "bradbury_sub",
                            self.subscriber,
                            str(xMsgConstants.REGISTER_SUBSCRIBER),
                            str(xMsgConstants.REGISTER_REQUEST_TIMEOUT))

    def test_send_local_publisher_removal(self):
        self.driver.remove_registration_local("bradbury_pub", self.publisher,
                                              True)

        self.assert_request(self.ln_connection,
                            "bradbury_sub",
                            self.publisher,
                            str(xMsgConstants.REMOVE_PUBLISHER),
                            str(xMsgConstants.REMOVE_REQUEST_TIMEOUT))

    def test_send_frontend_publisher_removal(self):
        self.driver.remove_registration_fe("bradbury_pub", self.publisher,
                                           True)

        self.assert_request(self.fe_connection,
                            "bradbury_sub",
                            self.publisher,
                            str(xMsgConstants.REMOVE_PUBLISHER),
                            str(xMsgConstants.REMOVE_REQUEST_TIMEOUT))

    def test_send_local_subscriber_removal(self):
        self.driver.remove_registration_local("bradbury_sub", self.subscriber,
                                              False)

        self.assert_request(self.ln_connection,
                            "bradbury_sub",
                            self.subscriber,
                            str(xMsgConstants.REMOVE_SUBSCRIBER),
                            str(xMsgConstants.REMOVE_REQUEST_TIMEOUT))

    def test_send_frontend_subscriber_removal(self):
        self.driver.remove_registration_fe("bradbury_sub", self.subscriber, False)

        self.assert_request(self.fe_connection,
                            "bradbury_sub",
                            self.subscriber,
                            str(xMsgConstants.REMOVE_SUBSCRIBER),
                            str(xMsgConstants.REMOVE_REQUEST_TIMEOUT))

    def test_send_host_removal(self):
        self.driver.remove_all_registration_fe("10.2.9.1", "10.2.9.1_node")

        self.assert_request(self.fe_connection,
                            "10.2.9.91_node",
                            "10.2.9.1",
                            str(xMsgConstants.REMOVE_ALL_REGISTRATION),
                            str(xMsgConstants.REMOVE_REQUEST_TIMEOUT))

    def test_send_local_publisher_find(self):
        self.driver.find_local("10.2.9.1_node", self.publisher, True)

        self.assert_request(self.ln_connection,
                            "bradbury_pub",
                            self.publisher,
                            str(xMsgConstants.FIND_PUBLISHER),
                            str(xMsgConstants.FIND_REQUEST_TIMEOUT))

    def test_send_fe_publisher_find(self):
        self.driver.find_global("10.2.9.1_node", self.publisher, True)

        self.assert_request(self.fe_connection,
                            "bradbury_pub",
                            self.publisher,
                            str(xMsgConstants.FIND_PUBLISHER),
                            str(xMsgConstants.FIND_REQUEST_TIMEOUT))

    def test_send_local_subscriber_find(self):
        self.driver.find_local("10.2.9.1_node", self.subscriber, False)

        self.assert_request(self.ln_connection,
                            "bradbury_sub",
                            self.subscriber,
                            str(xMsgConstants.FIND_SUBSCRIBER),
                            str(xMsgConstants.FIND_REQUEST_TIMEOUT))

    def test_send_fe_subscriber_find(self):
        self.driver.find_global("10.2.9.1_node", self.subscriber, False)

        self.assert_request(self.fe_connection,
                            "bradbury_sub",
                            self.subscriber,
                            str(xMsgConstants.FIND_SUBSCRIBER),
                            str(xMsgConstants.FIND_REQUEST_TIMEOUT))

    def test_get_registration_from_local(self):
        self.set_response(xMsgRegResponse("", "", [self.publisher]))
        res = self.driver.find_local("10.2.9.1_node", self.publisher, True)
        self.assertEqual(res.get_data()[0], self.publisher)

    def test_get_registration_from_fe(self):
        self.set_response(xMsgRegResponse("", "", [self.publisher]))
        res = self.driver.find_global("10.2.9.1_node", self.publisher, True)
        self.assertEqual(res.get_data()[0], self.publisher)

    def assert_request(self, socket, name, data, topic, timeout):
        request_object = xMsgRegRequest(topic, name, data)

        self.driver._request(socket, request_object, timeout)
        verify(self.driver)._request(socket, request_object, timeout)

    def set_response(self, response):
        when(self.driver)._request(any(zmq.Socket),
                                   any(xMsgRegRequest),
                                   any(int)).thenReturn(response)

if __name__ == "__main__":
    unittest.main()
