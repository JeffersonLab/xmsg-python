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

import zmq
import threading

from xmsg.core.xMsgExceptions import ConnectionException
from xmsg.core.xMsgMessage import xMsgMessage


class Handler(threading.Thread):

    def __init__(self, socket, topic, handle):
        super(Handler, self).__init__(name=topic)
        self.socket = socket
        self.topic = topic
        self.__is_running = threading.Event()
        self.handle = handle

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def run(self):
        while not self.stopped():
            try:
                socks = dict(self.poller.poll())

                if socks.get(self.socket) == zmq.POLLIN:
                    msg = xMsgMessage.create_with_serialized_data(self.socket.recv_multipart())
                    self.handle(msg)
                    del msg

            except zmq.error.ZMQError as zmq_e:
                raise zmq.error.ZMQError("xMsgSubscription : %s" % zmq_e)

            except zmq.ContextTerminated as e:
                print "xMsgSubscription : %s" % e

    def stop(self):
        self.__is_running.set()

    def stopped(self):
        return self.__is_running.is_set()


class xMsgSubscription:

    def __init__(self, name, connection, topic):
        self.name = name
        self.socket = connection.get_sub_sock()
        self.topic = str(topic)

        if self.socket:
            self.socket.setsockopt(zmq.SUBSCRIBE, self.topic)

        else:
            raise ConnectionException

    def set_handle(self, handle):
        self.handle = handle
        self.thread = Handler(self.socket, self.topic, self.handle)

    def stop(self):
        self.thread.stop()
        self.socket.setsockopt(zmq.UNSUBSCRIBE, self.topic)

    def start(self):
        self.thread.start()

    def is_alive(self):
        return not self.thread.stopped()

    def __str__(self):
        return str(self.name)
