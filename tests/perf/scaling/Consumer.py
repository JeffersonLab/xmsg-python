# coding=utf-8

import multiprocessing as mp

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.net.xMsgAddress import ProxyAddress


class Publisher(xMsg):

    def __init__(self, proxy_address):
        super(Publisher, self).__init__(name="publisher")
        self.connection = self.get_connection(proxy_address)

    def reply(self, msg):
        self.publish(self.connection, msg)


class Consumer(xMsg):
    def __init__(self, pool_size, proxy_port):
        proxy_address = ProxyAddress("localhost", proxy_port)
        super(Consumer, self).__init__(name="the_consumer",
                                       proxy_address=proxy_address,
                                       pool_size=pool_size)
        self.connection = self.get_connection(proxy_address)
        self.queue = mp.Queue()

    class _CallBack(xMsgCallBack):

        def __init__(self, proxy_address):
            self.flag = False
            self.publisher = None
            self.proxy_address = proxy_address

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
                self.publisher = Publisher(self.proxy_address)
                self.flag = True

            # send back the message to producer
            self._fact(10000)
            msg.topic = "the_reply"
            self.publisher.reply(msg)

    def run(self):
        subscription = None
        try:
            subscription = self.subscribe(self.default_proxy_address,
                                          "the_producer",
                                          self._CallBack(self.default_proxy_address))
            xMsgUtil.keep_alive()
        except KeyboardInterrupt:
            self.unsubscribe(subscription)
            self.destroy()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.description = "Subscriber for scaling tests"
    parser.add_argument("pool_size", help="pool size for subscriber", type=int)
    parser.add_argument("--proxy-port", help="proxy port",
                        type=int, default=7791)
    args = parser.parse_args()

    C = Consumer(args.pool_size, args.proxy_port)
    C.run()
