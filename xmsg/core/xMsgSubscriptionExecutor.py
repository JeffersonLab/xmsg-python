# coding=utf-8

from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgUtil import xMsgUtil


class Executor(object):

    def __init__(self, queue, queue_interr, callback):
        self._callback = callback
        self._queue = queue
        self._queue_interr = queue_interr

    def run(self):
        try:
            while True:
                try:
                    s_msg = self._queue.get()
                    if s_msg:
                        self._queue.task_done()

                        if s_msg == u"STOP":
                            xMsgUtil.log("Worker received stop message")
                            self._queue_interr.put("excp")
                            return

                        msg = xMsgMessage.from_serialized_data(s_msg)
                        self._callback.callback(msg)

                except KeyboardInterrupt:
                    # executor process catches ctrl-c from subscriber
                    self._queue_interr.put("excp")
                    return
        except IOError:
            pass
        return
