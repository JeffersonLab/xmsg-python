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
import threading

from xmsg.core.xMsgExceptions import ConnectionException
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil

class xMsgSubscription:

    socket = str(xMsgConstants.UNDEFINED)
    topic = str(xMsgConstants.UNDEFINED)
    thread = str(xMsgConstants.UNDEFINED)
    
    class Handler(threading.Thread):
        is_running = False
        
        def run(self):
            while self.is_running:
                pass
        
        def start(self):
            self.is_running = True
            pass
        
        def stop(self):
            pass
        
        def is_alive(self):
            return self.is_running

    def __init__(self, name, connection, topic):
        self.socket = connection.get_pub_sock()
        if self.socket is None:
            raise ConnectionException
        self.socket.setsockopt(zmq.SUBSCRIBE, str(topic))
        xMsgUtil.sleep(0.5)
        self.topic = str(topic)
        self.thread = None 
