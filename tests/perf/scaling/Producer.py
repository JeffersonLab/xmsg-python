# coding=utf-8

import random
import time

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data.xMsgData_pb2 import xMsgData
from xmsg.net.xMsgAddress import ProxyAddress


class Producer(xMsg):

    def __init__(self, n_messages, proxy_port):
        proxy_address = ProxyAddress("localhost", proxy_port)
        super(Producer, self).__init__(name="the_producer",
                                       proxy_address=proxy_address)
        connection = self.get_connection(proxy_address)

        class _CallBack(xMsgCallBack):
            def __init__(self):
                super(_CallBack, self).__init__()
                self.count = 0
                self.alert_count = n_messages
                self.start_time = 0

            def callback(self, msg):
                if self.count == 0:
                    self.start_time = time.time()
                else:
                    if self.count % self.alert_count == 0:
                        now = time.time()
                        elapsed = now - self.start_time
                        xMsgUtil.log("With %d messages: %s" % (n_messages,
                                                               elapsed))
                        self.start_time = time.time()

                self.count += 1
        subscription = self.subscribe(proxy_address, "the_reply", _CallBack(),
                                      1)
        while True:
            try:
                t_msg_data = xMsgData()
                t_msg_data.type = xMsgData.T_FLOATA
                data = [float(random.randint(1, 10)) for _ in range(int(10))]

                # Create transient data
                t_msg_data.FLOATA.extend(data)
                t_msg = xMsgMessage.from_xmsg_data(self.myname, t_msg_data)
                self.publish(connection, t_msg)
            except KeyboardInterrupt:
                self.unsubscribe(subscription)
                self.destroy()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.description = "Publisher for scaling tests"
    parser.add_argument("message_count", help="report after N given messages",
                        type=int)
    parser.add_argument("--proxy-port", help="proxy port", type=int,
                        default=7791)
    args = parser.parse_args()
    P = Producer(args.message_count, args.proxy_port)
