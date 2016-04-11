# coding=utf-8

import unittest

from xmsg.net.xMsgAddress import RegAddress, ProxyAddress
from xmsg.core.xMsgConstants import xMsgConstants as constants
from xmsg.core.xMsgUtil import xMsgUtil as util


class TestRegAddress(unittest.TestCase):

    def setUp(self):
        self.host = util.get_local_ip()
        self.key1 = "tcp://%s:%d" % (self.host, int(constants.REGISTRAR_PORT))
        self.key2 = "tcp://%s:7777" % self.host

    def test_RegAddress_empty_constructor(self):
        reg_addr = RegAddress()
        self.assertEqual(reg_addr.host, self.host)
        self.assertEqual(reg_addr.port, int(constants.REGISTRAR_PORT))
        self.assertEqual(reg_addr.address, self.key1)
        self.assertIsInstance(reg_addr, RegAddress)

    def test_RegAddress_constructor_only_with_hostname(self):
        reg_addr = RegAddress("localhost")
        self.assertEqual(reg_addr.host, self.host)
        self.assertEqual(reg_addr.port, int(constants.REGISTRAR_PORT))
        self.assertEqual(reg_addr.address, self.key1)
        self.assertIsInstance(reg_addr, RegAddress)

    def test_RegAddress_constructor_with_all_parameters(self):
        reg_addr = RegAddress("localhost", 7771)
        self.assertEqual(reg_addr.host, self.host)
        self.assertEqual(reg_addr.port, 7771)
        self.assertIsInstance(reg_addr, RegAddress)
        reg_addr = RegAddress("localhost", 7777)
        self.assertEqual(reg_addr.host, self.host)
        self.assertEqual(reg_addr.address, self.key2)
        self.assertEqual(reg_addr.port, 7777)
        self.assertIsInstance(reg_addr, RegAddress)

    def test__equal__operator_true(self):
        reg_1 = RegAddress("1.1.1.1", 80)
        reg_2 = RegAddress("1.1.1.1", 80)
        self.assertEqual(reg_1, reg_2)

    def test__equal__operator_false(self):
        reg_1 = RegAddress("1.1.1.2", 80)
        reg_2 = RegAddress("1.1.1.1", 81)
        self.assertNotEqual(reg_1, reg_2)


class TestProxyAddress(unittest.TestCase):

    def setUp(self):
        self.host = util.get_local_ip()

    def test_ProxyAddress_empty_constructor(self):
        proxy_addr = ProxyAddress()
        self.assertEqual(proxy_addr.host, self.host)
        self.assertEqual(proxy_addr.pub_port, int(constants.DEFAULT_PORT))
        self.assertEqual(proxy_addr.sub_port, int(constants.DEFAULT_PORT) + 1)
        self.assertIsInstance(proxy_addr, ProxyAddress)

    def test_ProxyAddress_constructor_only_with_hostname(self):
        proxy_addr = ProxyAddress("localhost")
        self.assertEqual(proxy_addr.host, self.host)
        self.assertEqual(proxy_addr.pub_port, int(constants.DEFAULT_PORT))
        self.assertEqual(proxy_addr.sub_port, int(constants.DEFAULT_PORT) + 1)
        self.assertIsInstance(proxy_addr, ProxyAddress)

    def test_ProxyAddress_constructor_only_with_hostname_and_pub_port(self):
        proxy_addr = ProxyAddress("localhost", 1111)
        self.assertEqual(proxy_addr.host, self.host)
        self.assertEqual(proxy_addr.pub_port, 1111)
        self.assertEqual(proxy_addr.sub_port, 1112)
        self.assertIsInstance(proxy_addr, ProxyAddress)

    def test_ProxyAddress_constructor_only_with_hostname_and_pub_port_and_sub_port(self):
        proxy_addr = ProxyAddress("localhost", 1111, 2222)
        self.assertEqual(proxy_addr.host, self.host)
        self.assertEqual(proxy_addr.pub_port, 1111)
        self.assertEqual(proxy_addr.sub_port, 2222)
        self.assertIsInstance(proxy_addr, ProxyAddress)

    def test__equal__operator_true(self):
        reg_1 = ProxyAddress("1.1.1.1", 80)
        reg_2 = ProxyAddress("1.1.1.1", 80)
        self.assertEqual(reg_1, reg_2)
        reg_1 = ProxyAddress("1.1.1.1", 81)
        reg_2 = ProxyAddress("1.1.1.1", 81)
        self.assertEqual(reg_1, reg_2)

    def test__equal__operator_false(self):
        reg_1 = ProxyAddress("1.1.1.2", 80)
        reg_2 = ProxyAddress("1.1.1.1", 80)
        self.assertNotEqual(reg_1, reg_2)
        reg_1 = ProxyAddress("1.1.1.1", 80)
        reg_2 = ProxyAddress("1.1.1.1", 81)
        self.assertNotEqual(reg_1, reg_2)


if __name__ == "__main__":
    unittest.main()
