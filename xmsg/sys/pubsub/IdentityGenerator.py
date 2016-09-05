# coding=utf-8
import sys
from random import randint

from xmsg.core.xMsgUtil import xMsgUtil


class IdentityGenerator(object):

    @staticmethod
    def _get_ctrl_id_prefix():
        python_id = 3
        localhost = xMsgUtil.host_to_ip("localhost")
        ip_hash = int(hash(localhost)) & sys.maxint
        return python_id * 100000000 + (ip_hash % 1000) * 100000

    @staticmethod
    def get_ctrl_id():
        return IdentityGenerator._get_ctrl_id_prefix() + randint(0, 100000)
