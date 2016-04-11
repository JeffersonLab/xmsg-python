# coding=utf-8

import unittest
import zmq

from xmsg.core.ConnectionManager import ConnectionManager as CM
from xmsg.net.xMsgConnectionSetup import xMsgConnectionSetup
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress
from xmsg.net.xMsgConnection import xMsgConnection
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver


class TestConnectionManager(unittest.TestCase):

    def test_connection_constructor(self):
        connection_manager = CM(zmq.Context.instance())
        self.assertIsInstance(connection_manager, CM)

    def test_get_proxy_connection(self):
        connection_manager = CM(zmq.Context.instance())
        proxy = connection_manager.get_proxy_connection(ProxyAddress(),
                                                        xMsgConnectionSetup())
        self.assertIsInstance(proxy, xMsgConnection)

    def test_get_registrar_connection(self):
        connection_manager = CM(zmq.Context.instance())
        registrar = connection_manager.get_registrar_connection(RegAddress())
        self.assertIsInstance(registrar, xMsgRegDriver)


if __name__ == "__main__":
    unittest.main()
