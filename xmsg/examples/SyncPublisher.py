# coding=utf-8

import random
import time

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data.xMsgData_pb2 import xMsgData
from xmsg.net.xMsgAddress import ProxyAddress


def main(array_size, proxy_host, alert_every_n):
    """Publisher usage:
    ::
        Usage: python xmsg/examples/Publisher <array_size> <fe_host>
    """

    sync_publisher = xMsg("test_publisher")

    # Create a socket connections to the xMsg node
    connection = sync_publisher.get_connection(ProxyAddress(proxy_host))

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    # Publish data for ever...
    count = 0
    start_time = time.time()
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

            if count % alert_every_n == 0:
                now = time.time()
                elapsed = now - start_time
                xMsgUtil.log("With %d messages: %s" % (alert_every_n, elapsed))
                start_time = time.time()

        except KeyboardInterrupt:
            print ""
            xMsgUtil.log("Removing Registration and terminating thread pool.")
            sync_publisher.destroy()
            return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.description = "Example synchronous publisher for xMsg"
    parser.add_argument("array_size", help="size of array to publish", type=int)
    parser.add_argument("proxy_host", help="proxy host", type=str)
    parser.add_argument("--alert_every",
                        help="every n i will let you know the time", type=int,
                        default=100)

    args = parser.parse_args()
    main(args.array_size, args.proxy_host, args.alert_every)
