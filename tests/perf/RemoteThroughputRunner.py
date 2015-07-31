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

from xmsg.core.xMsgUtil import xMsgUtil
from tests.perf.RemoteThroughput import runner


def remote_runner(bind_to, message_size, start_message_count,
                  final_message_count, step):
    if start_message_count > final_message_count:
        return

    current_message_count = start_message_count

    while True:
        try:
            runner(bind_to, message_size, current_message_count)
        except KeyboardInterrupt:
            print "Exiting remote runner"
            return
        current_message_count += step
        xMsgUtil.sleep(20)
        if current_message_count >= final_message_count:
            break


def main():
    if len(sys.argv) == 6:
        remote_runner(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
                      int(sys.argv[4]), int(sys.argv[5]))
    else:
        print "usage: python RemoteThroughputRunner.py <bind-to> "\
            "<message-size> <start-message-count> <final-message-count> <step>"

if __name__ == '__main__':
    main()
