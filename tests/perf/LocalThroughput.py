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
import zmq
from threading import Condition

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.net.xMsgAddress import xMsgAddress


class Timer:
    nr = 1
    watch = 0
    elapsed = 0


class Subscriber(xMsg):

    myName = "throughput_subscriber"

    def __init__(self, bind_to, csv_flag=False):
        super(Subscriber, self).__init__(self.myName, bind_to, "localhost",
                                         pool_size=1)


class THRCallBack(xMsgCallBack):
    def __init__(self, csv_flag, messages, message_size, condition):
        self.timer = Timer()
        self.csv_flag = csv_flag
        self.message_count = int(messages)
        self.message_size = int(message_size)
        self.condition = condition

        if csv_flag:
            print "message_size;number_of_messages;mean_transfer_time[us];"\
                "mean_transfer_rate[msg/s];mean_throughput[Mb/s]"

    def callback(self, msg):
        if self.timer.nr == 1:
            self.condition.acquire()
            self.timer.watch = zmq.Stopwatch()
            self.timer.watch.start()
            self.timer.nr += 1

        elif self.timer.nr == self.message_count:
            self.timer.elapsed = self.timer.watch.stop()

            self.condition.notifyAll()
            self.condition.release()

        else:
            self.timer.nr += 1
        return msg

    def write(self):
        self.timer.elapsed = float(self.timer.elapsed)
        throughput = float(self.message_count) / self.timer.elapsed * 1000000
        megabits_per_sec = float(throughput * self.message_size * 8) / 1000000
        latency = float(self.timer.elapsed / self.message_count)

        if self.csv_flag:
            print "%d;%d;%f;%s;%s" % (self.message_size, self.timer.nr,
                                      latency, str(throughput),
                                      str(megabits_per_sec))

        else:
            print "message size: %d " % self.message_size
            print "message count: %d" % self.timer.nr
            print "mean transfer time: %f [us]" % latency
            print "mean transfer rate: %s [msg/s]" % str(throughput)
            print "mean throughput: %s [Mb/s]" % str(megabits_per_sec)


def local_runner(bind_to, size_message, n_messages, csv_flag=False):
    subscriber = Subscriber(bind_to, csv_flag)

    pub_node = xMsgAddress(bind_to)
    connection = subscriber.get_new_connection(pub_node)
    topic = xMsgTopic.wrap("thr_topic")

    condition = Condition()
    callback = THRCallBack(csv_flag, n_messages, size_message, condition)
    try:
        subscription = subscriber.subscribe(connection, topic, callback)

        with condition:
            condition.wait()
        callback.write()
    except:
        print "Exiting..."
    finally:
        subscriber.unsubscribe(subscription)
        subscriber.destroy()
        return


def main():
    if len(sys.argv) == 5:
        if sys.argv[4] == "--csv-output":
            local_runner(sys.argv[1], sys.argv[2], sys.argv[3], True)

        else:
            print "usage: python LocalThoughput.py <bind-to> <message_size> <number_messages> [--csv-output]"

    elif len(sys.argv) == 4:
        local_runner(sys.argv[1], sys.argv[2], sys.argv[3])

    else:
        print "usage: python LocalThoughput.py <bind-to> <message_size> <number_messages> [--csv-output]"
        return -1

if __name__ == '__main__':
    main()
