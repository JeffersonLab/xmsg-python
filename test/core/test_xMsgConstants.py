import unittest
from core.xMsgConstants import xMsgConstants


class TestXMsgConstants(unittest.TestCase):

    def test_constants_value(self):
        self.assertEqual(0, int(xMsgConstants.UNDEFINED))
        self.assertEqual(1, int(xMsgConstants.SUCCESS))
        self.assertEqual(2, int(xMsgConstants.ANY))
        self.assertEqual(3, int(xMsgConstants.REGISTRAR))
        self.assertEqual(4, int(xMsgConstants.REGISTER_PUBLISHER))
        self.assertEqual(5, int(xMsgConstants.REGISTER_SUBSCRIBER))
        self.assertEqual(6, int(xMsgConstants.REMOVE_PUBLISHER))
        self.assertEqual(7, int(xMsgConstants.REMOVE_SUBSCRIBER))
        self.assertEqual(8, int(xMsgConstants.REMOVE_ALL_REGISTRATION))
        self.assertEqual(9, int(xMsgConstants.FIND_PUBLISHER))
        self.assertEqual(10, int(xMsgConstants.FIND_SUBSCRIBER))
        self.assertEqual(11, int(xMsgConstants.INFO))
        self.assertEqual(12, int(xMsgConstants.WARNING))
        self.assertEqual(13, int(xMsgConstants.ERROR))
        self.assertEqual(14, int(xMsgConstants.NO_RESULT))
        self.assertEqual(15, int(xMsgConstants.DONE))
        self.assertEqual(16, int(xMsgConstants.DATA))
        self.assertEqual(17, int(xMsgConstants.BIND))
        self.assertEqual(18, int(xMsgConstants.CONNECT))
        self.assertEqual(3000, int(xMsgConstants.REMOVE_REQUEST_TIMEOUT))
        self.assertEqual(3000, int(xMsgConstants.FIND_REQUEST_TIMEOUT))
        self.assertEqual(7771, int(xMsgConstants.DEFAULT_PORT))
        self.assertEqual(8888, int(xMsgConstants.REGISTRAR_PORT))

    def test_constants_label(self):
        self.assertEqual("undefined", str(xMsgConstants.UNDEFINED))
        self.assertEqual("success", str(xMsgConstants.SUCCESS))
        self.assertEqual("*", str(xMsgConstants.ANY))
        self.assertEqual("xMsg_Registrar", str(xMsgConstants.REGISTRAR))
        self.assertEqual("registerPublisher",
                         str(xMsgConstants.REGISTER_PUBLISHER))
        self.assertEqual("registerSubscriber",
                         str(xMsgConstants.REGISTER_SUBSCRIBER))
        self.assertEqual("removePublisherRegistration",
                         str(xMsgConstants.REMOVE_PUBLISHER))
        self.assertEqual("removeSubscriberRegistration",
                         str(xMsgConstants.REMOVE_SUBSCRIBER))
        self.assertEqual("removeAllRegistration",
                         str(xMsgConstants.REMOVE_ALL_REGISTRATION))
        self.assertEqual("findPublisher", str(xMsgConstants.FIND_PUBLISHER))
        self.assertEqual("findSubscriber", str(xMsgConstants.FIND_SUBSCRIBER))
        self.assertEqual("info", str(xMsgConstants.INFO))
        self.assertEqual("warning", str(xMsgConstants.WARNING))
        self.assertEqual("error", str(xMsgConstants.ERROR))
        self.assertEqual("none", str(xMsgConstants.NO_RESULT))
        self.assertEqual("done", str(xMsgConstants.DONE))
        self.assertEqual("data", str(xMsgConstants.DATA))
        self.assertEqual("bind", str(xMsgConstants.BIND))
        self.assertEqual("connect", str(xMsgConstants.CONNECT))
        self.assertEqual("removeRequestTimeout",
                         str(xMsgConstants.REMOVE_REQUEST_TIMEOUT))
        self.assertEqual("findRequestTimeout",
                         str(xMsgConstants.FIND_REQUEST_TIMEOUT))
        self.assertEqual("defaultPort", str(xMsgConstants.DEFAULT_PORT))
        self.assertEqual("registrarPort", str(xMsgConstants.REGISTRAR_PORT))

    def test_constants_get_string_value(self):
        self.assertEqual("undefined",
                         xMsgConstants.UNDEFINED.get_string_value())
        self.assertEqual("success",
                         xMsgConstants.SUCCESS.get_string_value())
        self.assertEqual("*", xMsgConstants.ANY.get_string_value())
        self.assertEqual("xMsg_Registrar",
                         xMsgConstants.REGISTRAR.get_string_value())
        self.assertEqual("registerPublisher",
                         xMsgConstants.REGISTER_PUBLISHER.get_string_value())
        self.assertEqual("registerSubscriber",
                         xMsgConstants.REGISTER_SUBSCRIBER.get_string_value())
        self.assertEqual("removePublisherRegistration",
                         xMsgConstants.REMOVE_PUBLISHER.get_string_value())
        self.assertEqual("removeSubscriberRegistration",
                         xMsgConstants.REMOVE_SUBSCRIBER.get_string_value())
        self.assertEqual("removeAllRegistration",
                         xMsgConstants.REMOVE_ALL_REGISTRATION.get_string_value())
        self.assertEqual("findPublisher",
                         xMsgConstants.FIND_PUBLISHER.get_string_value())
        self.assertEqual("findSubscriber",
                         xMsgConstants.FIND_SUBSCRIBER.get_string_value())
        self.assertEqual("info", xMsgConstants.INFO.get_string_value())
        self.assertEqual("warning", xMsgConstants.WARNING.get_string_value())
        self.assertEqual("error", xMsgConstants.ERROR.get_string_value())
        self.assertEqual("none", xMsgConstants.NO_RESULT.get_string_value())
        self.assertEqual("done", xMsgConstants.DONE.get_string_value())
        self.assertEqual("data", xMsgConstants.DATA.get_string_value())
        self.assertEqual("bind", xMsgConstants.BIND.get_string_value())
        self.assertEqual("connect", xMsgConstants.CONNECT.get_string_value())
        self.assertEqual("removeRequestTimeout",
                         xMsgConstants.REMOVE_REQUEST_TIMEOUT.get_string_value())
        self.assertEqual("findRequestTimeout",
                         xMsgConstants.FIND_REQUEST_TIMEOUT.get_string_value())
        self.assertEqual("defaultPort",
                         xMsgConstants.DEFAULT_PORT.get_string_value())
        self.assertEqual("registrarPort",
                         xMsgConstants.REGISTRAR_PORT.get_string_value())

    def test_constants_get_int_value(self):
        self.assertEqual(0, xMsgConstants.UNDEFINED.get_int_value())
        self.assertEqual(1, xMsgConstants.SUCCESS.get_int_value())
        self.assertEqual(2, xMsgConstants.ANY.get_int_value())
        self.assertEqual(3, xMsgConstants.REGISTRAR.get_int_value())
        self.assertEqual(4, xMsgConstants.REGISTER_PUBLISHER.get_int_value())
        self.assertEqual(5, xMsgConstants.REGISTER_SUBSCRIBER.get_int_value())
        self.assertEqual(6, xMsgConstants.REMOVE_PUBLISHER.get_int_value())
        self.assertEqual(7, xMsgConstants.REMOVE_SUBSCRIBER.get_int_value())
        self.assertEqual(8,
                         xMsgConstants.REMOVE_ALL_REGISTRATION.get_int_value())
        self.assertEqual(9, xMsgConstants.FIND_PUBLISHER.get_int_value())
        self.assertEqual(10, xMsgConstants.FIND_SUBSCRIBER.get_int_value())
        self.assertEqual(11, xMsgConstants.INFO.get_int_value())
        self.assertEqual(12, xMsgConstants.WARNING.get_int_value())
        self.assertEqual(13, xMsgConstants.ERROR.get_int_value())
        self.assertEqual(14, xMsgConstants.NO_RESULT.get_int_value())
        self.assertEqual(15, xMsgConstants.DONE.get_int_value())
        self.assertEqual(16, xMsgConstants.DATA.get_int_value())
        self.assertEqual(17, xMsgConstants.BIND.get_int_value())
        self.assertEqual(18, xMsgConstants.CONNECT.get_int_value())
        self.assertEqual(3000,
                         xMsgConstants.REMOVE_REQUEST_TIMEOUT.get_int_value())
        self.assertEqual(3000,
                         xMsgConstants.FIND_REQUEST_TIMEOUT.get_int_value())
        self.assertEqual(7771, xMsgConstants.DEFAULT_PORT.get_int_value())
        self.assertEqual(8888, xMsgConstants.REGISTRAR_PORT.get_int_value())
