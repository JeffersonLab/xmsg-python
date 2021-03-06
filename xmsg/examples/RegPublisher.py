# coding=utf-8

from random import randint

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2
from xmsg.net.xMsgAddress import RegAddress


def main():
    """Publisher usage:
    ::
        "Usage: python xmsg/examples/Publisher <array_size>
    """
    # Create an xMsg actor
    publisher = xMsg("test_publisher")

    # Create a socket connections to the xMsg node
    connection = publisher.connect()

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    # Register at xMsg Registrar
    reg_address = RegAddress()
    publisher.register_as_publisher(reg_address, topic)

    # Publish data for ever...
    while True:
        data = [float(randint(1, 10)) for _ in range(int(5))]

        # Create transient data
        t_msg_data = xMsgData_pb2.xMsgData()
        t_msg_data.type = xMsgData_pb2.xMsgData.T_FLOATA
        t_msg_data.FLOATA.extend(data)
        t_msg = xMsgMessage.from_xmsg_data(topic, t_msg_data)

        # Publishing
        publisher.publish(connection, t_msg)
        print "publishing : T_FLOATA"
        xMsgUtil.sleep(1)


if __name__ == '__main__':
    main()
