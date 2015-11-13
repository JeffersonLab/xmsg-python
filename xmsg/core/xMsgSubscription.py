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

from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgUtil import xMsgUtil


class Handler(threading.Thread):

    def __init__(self, topic, connection, handle):
        super(Handler, self).__init__(name=topic)
        self.connection = connection
        self.__is_running = threading.Event()
        self.handle = handle

        self.poller = zmq.Poller()
        self.poller.register(connection.sub, zmq.POLLIN)

    def run(self):
        while not self.stopped():
            try:
                socks = dict(self.poller.poll(100))

                if socks.get(self.connection.sub) == zmq.POLLIN:
                    received_data = self.connection.recv()
                    msg = xMsgMessage.create_with_serialized_data(received_data)
                    self.handle(msg)
                    del msg

            except zmq.error.ZMQError:
                if self.stopped():
                    xMsgUtil.log("Subscription stopped correctly.")
                    return

                else:
                    return

    def stop(self):
        self.__is_running.set()

    def stopped(self):
        return self.__is_running.is_set()


class xMsgSubscription:

    def __init__(self, topic, connection):
        self.connection = connection
        self.topic = str(topic)

        self.connection.subscribe(self.topic)

    def set_handle(self, handle):
        self.handle = handle
        self.handle_thread = Handler(self.topic, self.connection, self.handle)

    def stop(self):
        try:
            self.handle_thread.stop()
            self.connection.unsubscribe(self.topic)

        except Exception as e:
            print e
            return

    def start(self):
        self.handle_thread.start()

    def is_alive(self):
        return not self.handle_thread.stopped()

    def __str__(self):
        return str(self.name)
