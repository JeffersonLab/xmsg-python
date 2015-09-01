#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
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
import random

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.net.xMsgAddress import xMsgAddress
from xmsg.data import xMsgData_pb2


class ExampleSyncPublisher(xMsg):

    def __init__(self, fe_host):
        super(ExampleSyncPublisher, self).__init__("test_publisher",
                                                   "localhost",
                                                   fe_host)
        self.domain = "test_domain"
        self.subject = "test_subject"
        self.xtype = "test_type"


def main():
    """Publisher usage:
    ::
        Usage: python xmsg/examples/Publisher <array_size> <fe_host>
    """
    if len(sys.argv) >= 2:
        array_size = int(sys.argv[1])
        try:
            fe_host = sys.argv[2]

        except IndexError:
            fe_host = "localhost"

        sync_publisher = ExampleSyncPublisher(fe_host)

        # Create a socket connections to the xMsg node
        address = xMsgAddress(fe_host)
        con = sync_publisher.connect(address)

        # Build Topic
        topic = xMsgTopic.build(sync_publisher.domain,
                                sync_publisher.subject,
                                sync_publisher.xtype)

        # Publish data for ever...
        count = 0
        while True:
            try:
                t_msg_data = xMsgData_pb2.xMsgData()
                t_msg_data.type = xMsgData_pb2.xMsgData.T_FLOATA
                data = [float(random.randint(1, 10)) for _ in range(array_size)]
                # Create transient data

                t_msg_data.FLOATA.extend(data)
                t_msg = xMsgMessage.create_with_xmsg_data(topic, t_msg_data)

                # Publishing
                sync_publisher.sync_publish(con, t_msg, 10)
                count += 1

            except KeyboardInterrupt:
                print "Removing Registration and terminating the thread pool."
                # sync_publisher.remove_publisher_registration(topic)
                sync_publisher.destroy()
                return
    else:
        print "Usage: python xmsg/examples/Publisher <array_size> <fe_host>"
        return

if __name__ == '__main__':
    main()
