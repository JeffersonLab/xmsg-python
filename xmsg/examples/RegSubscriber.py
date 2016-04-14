#

#


from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.data import xMsgData_pb2
from xmsg.core.xMsgExceptions import RegistrationException
from xmsg.net.xMsgAddress import RegAddress


class ExampleSubscriberCallback(xMsgCallBack):

    def callback(self, msg):
        # User takes care of the proper de-serialization
        ds_msg = xMsgData_pb2.xMsgData()
        ds_msg.ParseFromString(msg.get_data())
        print "Subscriber received data : \n%s" % ds_msg
        return msg


def main():
    subscriber = xMsg("test_subscriber")

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    # Register at xMsg Registrar
    reg_address = RegAddress()
    subscriber.register_as_subscriber(reg_address, topic)

    # Connect
    connection = subscriber.connect()

    try:
        if subscriber.find_publisher(reg_address, topic):
            callback = ExampleSubscriberCallback()
            subscription = subscriber.subscribe(topic, connection, callback)

            xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        subscriber.unsubscribe(subscription)
        subscriber.remove_as_subscriber(reg_address, topic)
        subscriber.destroy(10)
        return

    except RegistrationException:
        print "Unable to register"
        return -1


if __name__ == '__main__':
    main()
