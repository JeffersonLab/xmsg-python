import random
import sys

from core.xMsg import xMsg
from core.xMsgUtil import xMsgUtil
from core.xMsgMessage import xMsgMessage
from net.xMsgAddress import xMsgAddress


__author__ = 'gurjyan'


class Publisher(xMsg):

    # Object variables
    myName = "test_publisher"
    domain = "test_domain"
    subject = "test_subject"
    xtype = "test_type"

    def __init__(self, feHost="localhost"):
        xMsg.__init__(self, feHost)


def main():
    publisher = Publisher()

    # Create a socket connections to the xMsg node
    address = xMsgAddress()

    con = publisher.connect(address)

    # Register this publisher
    publisher.register_publisher(publisher.myName,
                                 publisher.domain,
                                 publisher.subject,
                                 publisher.xtype)

    # Create array of integers as a message payload.
    # The only argument defines the array size.
    size = sys.argv[1]
    topic = xMsgUtil.build_topic(publisher.domain,
                                 publisher.subject,
                                 publisher.xtype)
    # Create transient data
    t_msg = xMsgMessage(topic)
    t_msg.sender = publisher.myName


    for i in range(0, int(size)):
        #t_data.FLSINT32A.append(random.randint(1, 10))
        t_msg.set_data(random.randint(1, 10))

    # Publish data for ever...
    while True:
        try:
            publisher.publish_new(con, t_msg)
            xMsgUtil.sleep(1)
            print "publishing..."
        except KeyboardInterrupt:
            publisher.remove_publisher_registration(publisher.myName,
                                                    publisher.domain,
                                                    publisher.subject,
                                                    publisher.xtype)
            print "Me sali de publisher..."
            break
    return

if __name__ == '__main__':
    main()
    
