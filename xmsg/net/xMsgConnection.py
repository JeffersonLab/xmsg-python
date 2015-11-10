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

import zmq


class xMsgConnection:

    def __init__(self, address, setup, pub_socket, sub_socket):
        self.address = address
        self.setup = setup
        self.pub = pub_socket
        self.sub = sub_socket

    def connect(self):
        self.setup.pre_connection(self.pub)
        self.setup.pre_connection(self.sub)

        pub_port = str(self.address.pub_port)
        sub_port = str(self.address.sub_port)

        self.pub.connect("tcp://%s:%s" % (self.address.host, pub_port))
        self.sub.connect("tcp://%s:%s" % (self.address.host, sub_port))

        self.setup.post_connection()

    def send(self, message):
        topic = str(message.get_topic())
        meta = message.get_metadata().SerializeToString()
        data = message.get_data()

        self.pub.send(topic, zmq.SNDMORE)
        self.pub.send(meta, zmq.SNDMORE)
        self.pub.send(data)

    def recv(self):
        return self.sub.recv_multipart()

    def subscribe(self, topic):
        self.sub.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe(self, topic):
        self.sub.setsockopt(zmq.UNSUBSCRIBE, topic)

    def address(self):
        pass
