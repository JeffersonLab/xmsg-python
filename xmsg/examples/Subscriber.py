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
        print "Subscriber received data : %s" % ds_msg


def main():
    # Create an xMsg actor
    subscriber = xMsg("test_subscriber")

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    subscription = None
    try:
        subscription = subscriber.subscribe(ProxyAddress(),
                                            topic,
                                            ExampleSubscriberCallback())
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        subscriber.unsubscribe(subscription)
        subscriber.destroy()


if __name__ == "__main__":
    main()
