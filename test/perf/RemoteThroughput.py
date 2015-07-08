'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''
import sys

from core.xMsg import xMsg
from core.xMsgTopic import xMsgTopic
from core.xMsgMessage import xMsgMessage
from net.xMsgAddress import xMsgAddress


class Publisher(xMsg):

    # Object variables
    myName = "throughput_publisher"
    domain = "throughput_domain"
    subject = "throughput_subject"
    xtype = "throughput_type"    

    def __init__(self, bind_to ,msg_size, msg_count):
        xMsg.__init__(self, self.myName, bind_to, pool_size=1)
        self.message_size = msg_size
        self.message_count = msg_count

def main():
    if len(sys.argv) == 4:
        bind_to = sys.argv[1];
        message_size = int(sys.argv[2])
        message_count = long(sys.argv[3])

        publisher = Publisher(bind_to, message_size, message_count)

        pub_node_addr = xMsgAddress(bind_to)
        pub_connection = publisher.get_new_connection(pub_node_addr)
        topic = xMsgTopic.build(publisher.domain, publisher.subject, publisher.xtype)
        
        publisher.register_publisher(topic)
        data = bytes(b'\x00' * message_size)

        try:
            for _ in range(message_count):
                t_msg = xMsgMessage.create_with_serialized_data(topic, data)
                print "publishing! (message size : " + str(sys.getsizeof(t_msg.get_data())) + ")"
                publisher.publish(pub_connection, t_msg)

        except:
            print "Removing publisher..."
            publisher.remove_publisher_registration(topic)

    else:
        print "usage: remote_thr <bind-to> <message-size> <message-count>"
        return -1

if __name__ == '__main__':
    main()
