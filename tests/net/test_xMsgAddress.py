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

from xmsg.net.xMsgAddress import RegAddress, ProxyAddress
from xmsg.core.xMsgConstants import xMsgConstants as constants
from xmsg.core.xMsgUtil import xMsgUtil as util


class TestRegAddress(unittest.TestCase):

    def setUp(self):
        self.host = util.get_local_ip()
        self.key1 = "%s:%d" % (self.host, int(constants.DEFAULT_PORT))
        self.key2 = "%s:7777" % self.host

    def test_RegAddress_empty_constructor(self):
        reg_addr = RegAddress()
        self.assertEqual(reg_addr.get_host(), self.host)
        self.assertEqual(reg_addr.get_port(), 7771)
        self.assertEqual(reg_addr.get_key(), self.key1)
        self.assertIsInstance(reg_addr, RegAddress)

    def test_RegAddress_constructor_only_with_hostname(self):
        reg_addr = RegAddress("localhost")
        self.assertEqual(reg_addr.get_host(), self.host)
        self.assertEqual(reg_addr.get_port(), 7771)
        self.assertEqual(reg_addr.get_key(), self.key1)
        self.assertIsInstance(reg_addr, RegAddress)

    def test_RegAddress_constructor_with_all_parameters(self):
        reg_addr = RegAddress("localhost", 7771)
        self.assertEqual(reg_addr.get_host(), self.host)
        self.assertEqual(reg_addr.get_port(), 7771)
        self.assertIsInstance(reg_addr, RegAddress)
        reg_addr = RegAddress("localhost", 7777)
        self.assertEqual(reg_addr.get_host(), self.host)
        self.assertEqual(reg_addr.get_key(), self.key2)
        self.assertEqual(reg_addr.get_port(), 7777)
        self.assertIsInstance(reg_addr, RegAddress)


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


if __name__ == "__main__":
    unittest.main()
