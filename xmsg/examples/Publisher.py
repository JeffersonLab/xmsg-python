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

import random
import sys

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2
from xmsg.net.xMsgAddress import xMsgAddress


__author__ = 'gurjyan'


class Publisher(xMsg):
    """Publisher usage:
    ::
        python xmsg/examples/Publisher <size of array>
    """

    def __init__(self, fe_host="localhost"):
        xMsg.__init__(self, "test_publisher", fe_host)
        self.domain = "test_domain"
        self.subject = "test_subject"
        self.xtype = "test_type"


def main():
    publisher = Publisher()

    # Create a socket connections to the xMsg node
    address = xMsgAddress()
    con = publisher.connect(address)

    # Build Topic
    topic = xMsgTopic.build(publisher.domain, publisher.subject,
                            publisher.xtype)

    # Register this publisher
    publisher.register_publisher(topic)

    # Create array of integers as a message payload.
    # The only argument defines the array size.
    size = sys.argv[1]

    # Publish data for ever...
    while True:
        try:
            data = [float(random.randint(1, 10)) for _ in range(0, int(size))]

            # Create transient data
            t_msg_data = xMsgData_pb2.xMsgData()
            t_msg_data.type = xMsgData_pb2.xMsgData.T_FLOATA
            t_msg_data.FLOATA.extend(data)
            t_msg = xMsgMessage.create_with_xmsg_data(topic, t_msg_data)

            # Publishing
            publisher.publish(con, t_msg)
            print "publishing : T_FLOATA"
            xMsgUtil.sleep(1)

        except KeyboardInterrupt:
            print "Removing Registration and terminating the thread pool..."
            publisher.remove_publisher_registration(topic)
            publisher.destroy()
            return

if __name__ == '__main__':
    main()
