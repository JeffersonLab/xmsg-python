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
import random
import sys

from core.xMsg import xMsg
from core.xMsgUtil import xMsgUtil
from core.xMsgMessage import xMsgMessage
from net.xMsgAddress import xMsgAddress


__author__ = 'gurjyan'


class Publisher(xMsg):

    # Object variables
    myName = "test_publisher"
    domain = "test_domain"
    subject = "test_subject"
    xtype = "test_type"

    def __init__(self, feHost="localhost"):
        xMsg.__init__(self, feHost)


def main():
    publisher = Publisher()

    # Create a socket connections to the xMsg node
    address = xMsgAddress()
    con = publisher.connect(address)

    # Register this publisher
    print xMsgUtil.current_time() + " Info: Publisher says \"I wish i was a publisher :)\""
    publisher.register_publisher(publisher.myName,
                                 publisher.domain,
                                 publisher.subject,
                                 publisher.xtype)
    print xMsgUtil.current_time() + " Info: Publisher says \"Now i am a publisher :)\""

    # Create array of integers as a message payload.
    # The only argument defines the array size.
    size = sys.argv[1]
    topic = xMsgUtil.build_topic(publisher.domain,
                                 publisher.subject,
                                 publisher.xtype)
    # Create transient data
    t_msg = xMsgMessage(topic)
    t_msg.sender = publisher.myName

    data_type_array = ["T_STRING", "T_FLSINT32", "T_FLOAT", "T_FLSINT32A", "T_FLSINT64A",
                       "T_FLOATA", "T_BYTESA"]

    # Publish data for ever...
    while True:
        try:
            data_type_n = random.randint(0, 6)

            if data_type_n == 0:
                t_msg.set_data("some test string!!!")

            elif data_type_n == 1:
                t_msg.set_data(int(random.randint(1, 100)))

            elif data_type_n == 2:
                t_msg.set_data(long(random.randint(1,100)))

            elif data_type_n == 3:
                t_msg.set_data([random.randint(1, 10) for _ in range(0, int(size))])

            elif data_type_n == 4:
                t_msg.set_data([long(random.randint(1, 10)) for _ in range(0, int(size))])

            elif data_type_n == 5:
                t_msg.set_data([float(random.randint(1, 10)) for _ in range(0, int(size))])

            elif data_type_n == 6:
                t_msg.set_data(bytearray([0x00, 0x00, 0x00, 0x08, 0x00]))

            publisher.publish(con, t_msg)
            print "publishing : " + data_type_array[data_type_n]
            xMsgUtil.sleep(1)

        except KeyboardInterrupt:
            publisher.remove_publisher_registration(publisher.myName,
                                                    publisher.domain,
                                                    publisher.subject,
                                                    publisher.xtype)
            publisher.terminate_threadpool()
            return

if __name__ == '__main__':
    main()
