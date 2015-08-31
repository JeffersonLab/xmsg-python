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

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.net.xMsgAddress import xMsgAddress
from xmsg.data import xMsgData_pb2


class Timer:
    nr = -1
    watch = 0
    elapsed = 0

    def reset(self):
        self.nr = 1
        self.watch = 0
        self.elapsed = 0


class LocalSubscriber(xMsg):

    myName = "throughput_subscriber"

    def __init__(self, bind_to, csv_flag=False):
        super(LocalSubscriber, self).__init__(self.myName,
                                              bind_to,
                                              "localhost",
                                              pool_size=1)


class THRCallBack(xMsgCallBack):
    def __init__(self, csv_flag):
        self.timer = Timer()
        self.csv_flag = csv_flag

        if csv_flag:
            print "CSV output:"
            print "message_size;number_of_messages;mean_transfer_time[ms];"\
                "mean_transfer_rate[Mb/s];mean_throughput[msg/s]"

    def check_data_valid_size(self, message_data):
        if sys.getsizeof(message_data.get_data()) != self.message_size + 37:
            return False
        return True

    def config(self, msg_count, msg_size):
        self.message_count = msg_count
        self.message_size = msg_size

    def callback(self, msg):
        if str(msg.get_metadata().description) == 'config message':
            deserialized_msg = xMsgData_pb2.xMsgData()
            deserialized_msg.ParseFromString(msg.get_data())
            msg_count = deserialized_msg.FLSINT32A[0]
            msg_size = deserialized_msg.FLSINT32A[1]
            self.config(msg_count, msg_size)

            self.timer.watch = zmq.Stopwatch()
            self.timer.watch.start()
            self.timer.nr = 1

        elif str(msg.get_metadata().description) == 'data message end':
            self.timer.elapsed = self.timer.watch.stop()
            self.timer.elapsed = float(self.timer.elapsed) / 1000000

            throughput = float(self.message_count) / self.timer.elapsed
            megabits_per_sec = float(throughput * self.message_size * 8) / 1000000
            latency = float(self.timer.elapsed / self.message_count) * 1000.0

            if self.csv_flag:
                print "%d;%d;%f;%s;%s" % (self.message_size, self.timer.nr,
                                          latency, str(throughput),
                                          str(megabits_per_sec))

            else:
                print "message size: %d " % self.message_size
                print "message count: %d" % self.timer.nr
                print "mean transfer time: %f [ms]" % latency
                print "mean transfer rate: %s [Mb/s]" % str(megabits_per_sec)
                print "mean throughput: %s [message/s]" % str(throughput)
            self.timer.reset()

        else:
            self.timer.nr += 1

        return msg


def local_runner(bind_to, csv_flag=False):
    subscriber = LocalSubscriber(bind_to, csv_flag)

    pub_node = xMsgAddress(bind_to)
    connection = subscriber.get_new_connection(pub_node)
    topic = xMsgTopic.wrap("thr_topic")

    callback = THRCallBack(csv_flag)

    subscription = subscriber.subscribe(connection, topic, callback)

    try:
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        subscriber.unsubscribe(subscription)
        subscriber.destroy(5000)
        return


def main():
    if len(sys.argv) == 3:
        if sys.argv[2] == "--csv-output":
            local_runner(sys.argv[1], True)

        else:
            print "usage: python LocalThoughput.py <bind-to> [--csv-output]"

    elif len(sys.argv) == 2:
        local_runner(sys.argv[1])

    else:
        print "usage: python LocalThoughput.py <bind-to> [--csv-output]"
        return -1

if __name__ == '__main__':
    main()
