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
from xsys.regdis.xMsgRegistrationService import xMsgRegistrationService
import zmq
import time


class StressGetRegistration:

    def __init__(self, params):
        '''
        Constructor
        '''
        self.params = params

    def runner(self):
        print "Cases;RegEx;Nested Ifs"
        for param in self.params:
            self._setup(int(param))
            old_get = self.get_registration_publisher(int(param))
            old_get += self.get_registration_subscriber(int(param))
            new_get = self.get_registration_new_publisher(int(param))
            new_get += self.get_registration_new_subscriber(int(param))
            avg_new = new_get/2
            avg_old = old_get/2
            out = str(avg_new).replace(".", ",")
            out += ";" + str(avg_old).replace(".", ",")
            print str(param) + ";" + out
            self._clean()

    def _setup(self, n):
        self.r_service = xMsgRegistrationService(zmq.Context)
        for i in range(n):
            topic = "domain%s:subject%s:type%s" % (i, i, i)
            self.r_service._register(topic, "data_p", True)
            self.r_service._register(topic, "data_s", False)

    def _clean(self):
        del self.r_service

    def get_registration_publisher(self, n):
        start = time.time()
        for i in range(n):
            d = "domain%s" % i
            s = "subject%s" % i
            t = "type%s" % i
            self.r_service._get_registration(d, s, t, True)
        end = time.time()
        elapsed = end - start
        return elapsed

    def get_registration_subscriber(self, n):
        start = time.time()
        for i in range(n):
            d = "domain%s" % i
            s = "subject%s" % i
            t = "type%s" % i
            self.r_service._get_registration(d, s, t, False)
        end = time.time()
        elapsed = end - start
        return elapsed

    def get_registration_new_publisher(self, n):
        start = time.time()
        for i in range(n):
            d = "domain%s" % i
            s = "subject%s" % i
            t = "type%s" % i
            self.r_service._get_registration_new(d, s, t, True)
        end = time.time()
        elapsed = end - start
        return elapsed

    def get_registration_new_subscriber(self, n):
        start = time.time()
        for i in range(n):
            d = "domain%s" % i
            s = "subject%s" % i
            t = "type%s" % i
            self.r_service._get_registration_new(d, s, t, False)
        end = time.time()
        elapsed = end - start
        return elapsed

if __name__ == "__main__":
    args = [5, 10, 50, 100, 500, 1000, 5000, 10000]
    stress_test_runner = StressGetRegistration(args)
    stress_test_runner.runner()
