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

import zmq
import unittest

from xmsg.core.xMsgConnectionSetup import xMsgConnectionSetup

class TestxMsgConnectionSetup(unittest.TestCase):


    def test_check_socket_HWM_pub(self):
        ctx = zmq.Context.instance()
        sock = ctx.socket(zmq.PUB)
        curr_hwm_rcv = sock.RCVHWM
        curr_hwm_snd = sock.SNDHWM
        xMsgConnectionSetup.pre_connection(sock)
        self.assertNotEqual(curr_hwm_rcv, sock.RCVHWM)
        self.assertNotEqual(curr_hwm_snd, sock.SNDHWM)
        self.assertEqual(0, sock.get_hwm())


if __name__ == "__main__":
    unittest.main()