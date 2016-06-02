# coding=utf-8

import random

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data.xMsgData_pb2 import xMsgData
from xmsg.net.xMsgAddress import ProxyAddress


def main(array_size):
    """Publisher usage:
    ::
        Usage: python xmsg/examples/Publisher <array_size> <fe_host>
    """

    sync_publisher = xMsg("test_publisher")

    # Create a socket connections to the xMsg node
    connection = sync_publisher.get_connection(ProxyAddress())

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    # Publish data for ever...
    count = 0
    while True:
        try:
            t_msg_data = xMsgData()
            t_msg_data.type = xMsgData.T_FLOATA
            data = [float(random.randint(1, 10)) for _ in range(int(array_size))]
            # Create transient data

            t_msg_data.FLOATA.extend(data)
            transient_message = xMsgMessage.create_with_xmsg_data(topic,
                                                                  t_msg_data)

            # Publishing
            sync_publisher.sync_publish(connection, transient_message, 10)
            count += 1

        except KeyboardInterrupt:
            print ""
            xMsgUtil.log("Removing Registration and terminating thread pool.")
            sync_publisher.destroy()
            return


if __name__ == "__main__":
    main(10)
