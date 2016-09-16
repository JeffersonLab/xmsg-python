# coding=utf-8

import multiprocessing as mp

from xmsg.core.xMsgMessage import xMsgMessage


class Executor(mp.Process):

    def __init__(self, queue, callback):
        super(Executor, self).__init__(name="xmsg_worker")
        self._callback = callback
        self._queue = queue

    def run(self):
        while True:
            s_msg = self._queue.get()
            if s_msg == "STOP":
                return
            msg = xMsgMessage.from_serialized_data(s_msg)
            self._callback.callback(msg)
