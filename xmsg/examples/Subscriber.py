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

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.net.xMsgAddress import xMsgAddress
from xmsg.data import xMsgData_pb2

__author__ = 'gurjyan'


class Subscriber(xMsg):
    """Subscriber usage:
    ::
        python xmsg/examples/Subscriber
    """

    def __init__(self, fe_host="localhost"):
        xMsg.__init__(self, "test_publisher", fe_host)
        self.domain = "test_domain"
        self.subject = "test_subject"
        self.xtype = "test_type"

    def callback(self, msg):
        """Example of a callback function"""
        print "Subscriber received data : "
        # User takes care of the proper de-serialization
        ds_msg = xMsgData_pb2.xMsgData()
        ds_msg.ParseFromString(msg.get_data())
        print ds_msg


def main():
    subscriber = Subscriber()

    # Create a socket connections to the xMsg node
    address = xMsgAddress()
    con = subscriber.connect(address)

    # Build Topic
    topic = xMsgTopic.build(subscriber.domain, subscriber.subject,
                            subscriber.xtype)

    # Register this publisher
    subscriber.register_subscriber(topic)

    # Find a publisher that publishes to requested topic
    # defined as a static variables above
    if len(subscriber.find_local_publisher(topic)) > 0:

        # Subscribe by passing a callback to the subscription
        subscriber.subscribe(con, topic, subscriber.callback, True)

        try:
            xMsgUtil.keep_alive()

        except KeyboardInterrupt:
            subscriber.remove_subscriber_registration(topic)
            subscriber.destroy(2000)
            return

if __name__ == '__main__':
    main()
