# coding=utf-8

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data import xMsgData_pb2


class ExampleSubscriberCallback(xMsgCallBack):

    def callback(self, msg):
        # User takes care of the proper de-serialization
        ds_msg = xMsgData_pb2.xMsgData()
        ds_msg.ParseFromString(msg.data)
        print "Subscriber received data : %s" % ds_msg


def main():
    # Create an xMsg actor
    subscriber = xMsg("test_subscriber")

    # Create a socket connections to the xMsg node
    connection = subscriber.connect()

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    try:
        subscription = subscriber.subscribe(topic, connection, ExampleSubscriberCallback())
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        subscriber.unsubscribe(subscription)
        subscriber.destroy()


if __name__ == "__main__":
    main()
