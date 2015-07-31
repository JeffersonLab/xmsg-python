#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

import sys

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.net.xMsgAddress import xMsgAddress
from xmsg.data import xMsgData_pb2


class Publisher(xMsg):

    myName = "throughput_publisher"

    def __init__(self, bind_to, msg_size, msg_count):
        super(Publisher, self).__init__(self.myName, bind_to,
                                        pool_size=1)
        self.message_size = msg_size
        self.message_count = msg_count


def runner(bind_to, message_size, message_count):
    pub_node_addr = xMsgAddress(bind_to)
    publisher = Publisher(bind_to, message_size, message_count)
    pub_connection = publisher.get_new_connection(pub_node_addr)
    topic = xMsgTopic.wrap("thr_topic")

    subscriber_args = [message_count, message_size]
    configuration_data = xMsgData_pb2.xMsgData()
    configuration_data.type = xMsgData_pb2.xMsgData.T_FLSINT32A
    configuration_data.FLSINT32A.extend(subscriber_args)
    configuration_message = xMsgMessage.create_with_xmsg_data(topic,
                                                              configuration_data)
    publisher.publish(pub_connection, configuration_message)

    try:
        data = bytes(b'\x00' * message_size)
        for _ in range(message_count):
            t_msg = xMsgMessage.create_with_serialized_data(topic,
                                                            bytes(data))
            t_msg.set_mimetype("data/binary")
            publisher.publish(pub_connection, t_msg)

        publisher.destroy(30000)

    except Exception as e:
        print e
        print "Removing publisher..."
        publisher.destroy(0)

    return


def main():
    if len(sys.argv) == 4:
        runner(sys.argv[1], int(sys.argv[2]), long(sys.argv[3]))

    else:
        print "usage: remote_thr <bind-to> <message-size> <message-count>"
        return -1

if __name__ == '__main__':
    main()
