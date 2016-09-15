# coding=utf-8

import multiprocessing as mp

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.net.xMsgAddress import ProxyAddress


class Publisher(xMsg):

    def __init__(self):
        super(Publisher, self).__init__(name="publisher")
        self.connection = self.get_connection(ProxyAddress())

    def reply(self, msg):
        self.publish(self.connection, msg)


class Consumer(xMsg):
    def __init__(self, pool_size):
        super(Consumer, self).__init__(name="the_consumer",
                                       pool_size=pool_size)
        self.connection = self.get_connection(ProxyAddress())
        self.queue = mp.Queue()

    class _CallBack(xMsgCallBack):

        def __init__(self):
            self.flag = False
            self.publisher = None

        def _fact(self, n):
            fact = 0
            for i in range(n):
                if i == 0:
                    fact = 1
                else:
                    fact *= i
            return fact

        def callback(self, msg):
            if not self.flag:
                self.publisher = Publisher()
                self.flag = True

            # send back the message to producer
            self._fact(10000)
            msg.topic = "the_reply"
            self.publisher.reply(msg)

    def run(self):
        try:
            subscription = self.subscribe(ProxyAddress(),
                                          "the_producer",
                                          self._CallBack())
            xMsgUtil.keep_alive()
        except KeyboardInterrupt:
            self.destroy()
            self.unsubscribe(subscription)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.description = "Subscriber for scaling tests"
    parser.add_argument("pool_size", help="pool size for subscriber", type=int)
    args = parser.parse_args()

    C = Consumer(args.pool_size)
    C.run()
