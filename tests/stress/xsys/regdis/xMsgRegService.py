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

import time
from random import randint

from xmsg.sys.regdis.xMsgRegDatabase import xMsgRegDatabase
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data import xMsgRegistration_pb2


class StressGetRegistration:
    
    def __init__(self, params):
        self.params = params

    def runner(self):
        print "====================================="
        print " Avg response time for find register"
        print "====================================="
        print ""
        print "FIND: Exact Topic"
        for param in self.params:
            self._setup(int(param))
            regs_new = self.find_by_domain(self.publishers)[0]
            regs_new += self.find_by_domain(self.subscribers)[0]

            regs_old = self.find_by_domain(self.publishers)[1]
            regs_old += self.find_by_domain(self.subscribers)[1]

            avg_new = regs_new/2
            avg_old = regs_old/2
            out_new = str(avg_new).replace(".", ",")
            out_old = str(avg_old).replace(".", ",")

            print str(param) + ";" + out_new + ";" + out_old
            self._clean()
        print "FIND: By subject"
        for param in self.params:
            self._setup(int(param))
            regs_new = self.find_registration(self.publishers)[0]
            regs_new += self.find_registration(self.subscribers)[0]

            regs_old = self.find_by_subject(self.publishers)[1]
            regs_old += self.find_by_subject(self.subscribers)[1]

            avg_new = regs_new/2
            avg_old = regs_old/2
            out_new = str(avg_new).replace(".", ",")
            out_old = str(avg_old).replace(".", ",")

            print str(param) + ";" + out_new + ";" + out_old
            self._clean()
        print "FIND: By domain"
        for param in self.params:
            self._setup(int(param))
            regs_new = self.find_by_domain(self.publishers)[0]
            regs_new += self.find_by_domain(self.subscribers)[0]

            regs_old = self.find_by_domain(self.publishers)[1]
            regs_old += self.find_by_domain(self.subscribers)[1]

            avg_new = regs_new/2
            avg_old = regs_old/2
            out_new = str(avg_new).replace(".", ",")
            out_old = str(avg_old).replace(".", ",")

            print str(param) + ";" + out_new + ";" + out_old
            self._clean()

    def _setup(self, n):
        self.publishers = xMsgRegDatabase()
        self.subscribers = xMsgRegDatabase()
        self.randlist = [randint(0, n) for i in range(n)]
        self.db_old = dict()
        for i in self.randlist:
            self.publishers.register(self.register_data(i))
            self.subscribers.register(self.register_data(i))
            topic = "domain%s:subject%s:xtype%s" % (i, i, i)
            self.register_old(topic, "data")

    def _clean(self):
        del self.publishers
        del self.subscribers
        del self.db_old

    def find_registration(self, db):
        avg_new = 0
        avg_old = 0
        for i in self.randlist:
            d = "domain%s" % i
            s = "subject%s" % i
            t = "xtype%s" % i
            start = time.time()
            db.find(d, s, t)
            end = time.time()
            avg_new += (end - start)/len(self.randlist)

            start = time.time()
            self.find_old(d, s, t)
            end = time.time()
            avg_old += (end - start)/len(self.randlist)
        return [avg_new, avg_old]

    def find_by_subject(self, db):
        avg_new = 0
        avg_old = 0
        for i in self.randlist:
            d = "domain%s" % i
            s = "subject%s" % i
            t = "*"
            start = time.time()
            db.find(d, s, t)
            end = time.time()
            avg_new += (end - start)/len(self.randlist)

            start = time.time()
            self.find_old(d, s, t)
            end = time.time()
            avg_old += (end - start)/len(self.randlist)
        return [avg_new, avg_old]

    def find_by_domain(self, db):
        avg_new = 0
        avg_old = 0
        for i in self.randlist:
            d = "domain%s" % i
            s = "*"
            t = "*"

            start = time.time()
            db.find(d, s, t)
            end = time.time()
            avg_new += (end - start)/len(self.randlist)

            start = time.time()
            self.find_old(d, s, t)
            end = time.time()
            avg_old += (end - start)/len(self.randlist)
        return [avg_new, avg_old]

    def register_data(self, n):
        r_data = xMsgRegistration_pb2.xMsgRegistration()
        r_data.name = "name%s" % n
        r_data.description = "description"
        r_data.host = xMsgUtil.host_to_ip("localhost")
        r_data.port = 8888
        r_data.domain = "domain%s" % n
        r_data.subject = "subject%s" % n
        r_data.type = "xtype%s" % n
        return r_data

    def register_old(self, key, data):
        self.db_old[key] = data

    def find_old(self, domain, subject, tip):
        result = list()

        for k in self.db_old:
            topic = xMsgTopic.wrap(k)
            if ((topic.domain() == domain) and
                (topic.subject() == subject or
                 subject == "undefined" or subject == "*") and
                (topic.type() == tip or
                 tip == "undefined" or tip == "*")):
                result.append(self.db_old[k])
        return result

if __name__ == "__main__":
    args = [5, 10, 50, 100, 500, 1000, 5000, 10000]
    stress_test_runner = StressGetRegistration(args)
    stress_test_runner.runner()
