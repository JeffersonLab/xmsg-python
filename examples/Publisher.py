import random
import sys
from core.xMsg import xMsg
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from data import xMsgData_pb2
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
    publisher.registerPublisher(publisher.myName,
                                publisher.domain,
                                publisher.subject,
                                publisher.xtype)

    # Create array of integers as a message payload.
    # The only argument defines the array size.
    size = sys.argv[1]

    # Create transient data
    t_data = xMsgData_pb2.Data()
    t_data.author = publisher.myName
    t_data.id = 0
    t_data.dataDescription = xMsgConstants.UNDEFINED
    t_data.xtype = xMsgData_pb2.Data.T_FLSINT32A

    for i in range(0, int(size)):
        t_data.FLSINT32A.append(random.randint(1, 10))

    # Publish data for ever...
    while True:
        publisher.publish(con,
                          publisher.domain,
                          publisher.subject,
                          publisher.xtype,
                          publisher.myName,
                          t_data)
        xMsgUtil.sleep(1)
        print "publishing..."

if __name__ == '__main__':
    main()

