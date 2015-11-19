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

    def __init__(self, address, pub_socket, sub_socket):
        self.address = address
        self.pub = pub_socket
        self.sub = sub_socket

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_sub_socket(self):
        return self.sub

    def set_sub_socket(self, subcriber_socket):
        self.sub = subcriber_socket

    def get_pub_socket(self):
        return self.pub

    def set_pub_socket(self, publisher_socket):
        self.pub = publisher_socket

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
