from core.xMsg import xMsg
from core.xMsgUtil import xMsgUtil
from data import xMsgData_pb2
from net.xMsgAddress import xMsgAddress

__author__ = 'gurjyan'


class Subscriber(xMsg):

    # Object variables
    myName = "test_publisher"
    domain = "test_domain"
    subject = "test_subject"
    xtype = "test_type"

    def __init__(self, feHost="localhost"):
        xMsg.__init__(self, feHost)

    def callback(self, data):

        if data.type == xMsgData_pb2.xMsgData.T_FLSINT32A:
            print data.FLSINT32A


def main():
    subscriber = Subscriber()

    # Create a socket connections to the xMsg node
    address = xMsgAddress()
    con = subscriber.connect(address)

    # Register this publisher
    subscriber.register_subscriber(subscriber.myName,
                                   subscriber.domain,
                                   subscriber.subject,
                                   subscriber.xtype)

    # Find a publisher that publishes to requested topic
    # defined as a static variables above
    if len(subscriber.find_local_publisher(subscriber.myName,
                                           subscriber.domain,
                                           subscriber.subject,
                                           subscriber.xtype)) > 0:

        # Subscribe by passing a callback to the subscription
        subscriber.subscribe(con,
                             subscriber.domain,
                             subscriber.subject,
                             subscriber.xtype,
                             subscriber.callback,
                             True)
        try:
            xMsgUtil.keep_alive()
        except KeyboardInterrupt:
            print "saliendo..."
        finally:
            pass


if __name__ == '__main__':
    main()
