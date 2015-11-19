#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
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
