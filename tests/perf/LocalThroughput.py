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
import zmq
import threading

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.net.xMsgAddress import xMsgAddress


class Timer:
    nr = 0
    watch = 0
    elapsed = 0


class Subscriber(xMsg):

    # Object variables
    myName = "throughput_subscriber"
    domain = "throughput_domain"
    subject = "throughput_subject"
    xtype = "throughput_type"
    lock = threading.Lock()

    def __init__(self, bind_to, msg_size, msg_count):
        xMsg.__init__(self, self.myName, bind_to, pool_size=1)
        self.message_size = msg_size
        self.message_count = msg_count
        self.timer = Timer()

    def callback(self, msg):
        if sys.getsizeof(msg.get_data()) != self.message_size + 37:
            print (" incorrect size received " + str(sys.getsizeof(msg.get_data())) + ""
                  + " instead of : " +  str(self.message_size + 37))
            print msg.get_data()
            return -1

        self.timer.nr += 1

        if self.timer.nr == 1:
            self.timer.watch = zmq.Stopwatch()
            print "Calculating..."
            self.timer.watch.start()

        elif self.timer.nr == self.message_count:
            self.timer.elapsed = self.timer.watch.stop()
            self.timer.elapsed = float(self.timer.elapsed)/1000000

            throughput = float(self.message_count) / self.timer.elapsed
            megabits = float(throughput * self.message_size * 8) / 1000000
            latency = float(self.timer.elapsed / self.message_count)

            print "message size: %d " % self.message_size
            print "message count: %d" % self.message_count
            print "mean transfer time: %f [s]" % latency
            print "mean transfer rate: " + str(throughput) + " [msg/s]"
            print "mean throughput: " + str(megabits) + " [Mb/s]"
        return msg

def main():
    
    if len(sys.argv) == 4:
        
        bind_to = sys.argv[1];
        message_size = int(sys.argv[2]);
        message_count = long(sys.argv[3]);
        subscriber = Subscriber(bind_to, message_size, message_count)
    
        pub_node = xMsgAddress(bind_to)
        connection = subscriber.get_new_connection(pub_node)
        topic = xMsgTopic.build(subscriber.domain, subscriber.subject, subscriber.xtype)

        subscriber.register_subscriber(topic)
        
        subscriber.subscribe(connection,
                             topic,
                             subscriber.callback,
                             True)

        try:
            subscriber.lock.acquire()
            print "Waiting..."
            xMsgUtil.keep_alive()
            
        except KeyboardInterrupt:
            subscriber.remove_subscriber_registration(topic)
            return

    else:
        print "usage: local_thr <bind-to> <message-size> <message-count>"
        return -1

if __name__ == '__main__':
    main()
