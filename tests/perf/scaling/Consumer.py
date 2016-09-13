# coding=utf-8

import multiprocessing as mp

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.net.xMsgAddress import ProxyAddress


class Consumer(xMsg):
    def __init__(self, pool_size):
        super(Consumer, self).__init__(name="the_consumer",
                                       pool_size=pool_size)
        self.connection = self.get_connection(ProxyAddress())
        self.queue = mp.Queue()

        class _CallBack(xMsgCallBack):

            def __init__(self, q):
                super(_CallBack, self).__init__()
                self._queue = q

            def _fact(self, n):
                fact = 0
                for i in range(n):
                    if i == 0:
                        fact = 1
                    else:
                        fact *= i
                return fact

            def callback(self, msg):
                # send back the message to producer
                self._fact(6000)
                msg.topic = "the_reply"
                self._queue.put(msg.serialize())

        subscription = self.subscribe(ProxyAddress(),
                                      "the_producer",
                                      _CallBack(self.queue))
        try:
            while True:
                self.reply(self.queue.get())
        except KeyboardInterrupt:
            self.destroy()
            self.unsubscribe(subscription)

    def reply(self, s_msg):
        self.publish(self.connection,
                     xMsgMessage.create_with_serialized_data(s_msg))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.description = "Subscriber for scaling tests"
    parser.add_argument("pool_size", help="pool size for subscriber", type=int)
    args = parser.parse_args()

    C = Consumer(args.pool_size)
