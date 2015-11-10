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

from random import randint

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2


def main(array_size, frontend_host="localhost"):
    """Publisher usage:
    ::
        "Usage: python xmsg/examples/Publisher <array_size> <fe_host>
    """
    publisher = xMsg("test_publisher", "localhost", frontend_host)

    # Create a socket connections to the xMsg node
    connection = publisher.connect()

    # Build Topic
    topic = xMsgTopic.build("test_domain", "test_subject", "test_type")

    # Publish data for ever...
    while True:
        try:
            data = [float(randint(1, 10)) for _ in range(int(array_size))]

            # Create transient data
            t_msg_data = xMsgData_pb2.xMsgData()
            t_msg_data.type = xMsgData_pb2.xMsgData.T_FLOATA
            t_msg_data.FLOATA.extend(data)
            t_msg = xMsgMessage.create_with_xmsg_data(topic, t_msg_data)

            # Publishing
            publisher.publish(connection, t_msg)
            print "publishing : T_FLOATA"
            xMsgUtil.sleep(1)

        except KeyboardInterrupt:
            print ""
            xMsgUtil.log("Removing Registration and terminating thread pool")
            publisher.destroy()
            return
