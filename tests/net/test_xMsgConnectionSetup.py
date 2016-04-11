# coding=utf-8

import zmq
import unittest

from xmsg.net.xMsgConnectionSetup import xMsgConnectionSetup


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
