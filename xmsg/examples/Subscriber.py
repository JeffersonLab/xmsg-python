# coding=utf-8

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data.xMsgData_pb2 import xMsgData
from xmsg.net.xMsgAddress import ProxyAddress


class ExampleSubscriberCallback(xMsgCallBack):

    def callback(self, msg):
        # User takes care of the proper de-serialization
        ds_msg = xMsgData()
        ds_msg.ParseFromString(msg.data)
        return msg


def main(pool_size, proxy_host):
    # Create an xMsg actor
    subscriber = xMsg("test_subscriber", pool_size=pool_size)

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    subscription = None
    try:
        subscription = subscriber.subscribe(ProxyAddress(proxy_host), topic,
                                            ExampleSubscriberCallback())
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        subscriber.unsubscribe(subscription)
        subscriber.destroy()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.description = "Example subscriber for xMsg"
    parser.add_argument("pool_size", help="pool size for subscriber", type=int)
    parser.add_argument("proxy_host", help="proxy host to connect", type=str)
    args = parser.parse_args()

    main(args.pool_size, args.proxy_host)
