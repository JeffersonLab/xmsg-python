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
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.net.xMsgAddress import xMsgAddress
from xmsg.data import xMsgData_pb2
from xmsg.core.xMsgUtil import xMsgUtil


class ExampleSubscriber(xMsg):
    """Subscriber usage:
    ::
        python xmsg/examples/Subscriber <fe_host>
    """
    def __init__(self, fe_host, pool_size):
        super(ExampleSubscriber, self).__init__("test_publisher",
                                                "localhost",
                                                fe_host)
        self.domain = "test_domain"
        self.subject = "test_subject"
        self.xtype = "test_type"
        self.connection = self.connect(xMsgAddress(fe_host))


class ExampleSubscriberCallback(xMsgCallBack):

    def callback(self, msg):
        # User takes care of the proper de-serialization
        ds_msg = xMsgData_pb2.xMsgData()
        ds_msg.ParseFromString(msg.get_data())
        print "Subscriber received data : %s" % ds_msg
        return msg


def main():
    if len(sys.argv) is 2:
        fe_host = sys.argv[1]

    else:
        fe_host = "localhost"

    subscriber = ExampleSubscriber(fe_host=fe_host, pool_size=1)

    # Build Topic
    topic = xMsgTopic.build(subscriber.domain, subscriber.subject,
                            subscriber.xtype)

    # Register this publisher
    # subscriber.register_subscriber(topic)

    # Find a publisher that publishes to requested topic
    # defined as a static variables above
    #if subscriber.find_publisher(topic):
    # Subscribe by passing a callback to the subscription
    # subscriber.subscribe(con, topic, subscriber.callback, False)

    try:
        my_callback = ExampleSubscriberCallback()
        subscription = subscriber.subscribe(subscriber.connection,
                                            topic, my_callback)

        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        #subscriber.remove_subscriber_registration(topic)
        subscriber.unsubscribe(subscription)
        subscriber.destroy(10)
        return

if __name__ == '__main__':
    main()
