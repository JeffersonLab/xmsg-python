# coding=utf-8


class xMsgConnectionSetup(object):

    @staticmethod
    def pre_connection(socket):
        socket.set_hwm(0)

    @staticmethod
    def post_connection():
        pass
