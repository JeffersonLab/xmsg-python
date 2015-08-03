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
import sys

from xmsg.xsys.regdis.xMsgRegService import xMsgRegService
from xmsg.xsys.xMsgProxy import xMsgProxy
from xmsg.core.xMsgUtil import xMsgUtil


__author__ = 'gurjyan'


class xMsgRegistrar:
    """xMsgRegistrar, the main registrar service

    The service always runs in a separate thread. Contains two
    separate databases to store publishers and subscribers
    registration data. The key for the data base is xMsgTopic, constructed as:

    * *domain:subject:type*

    Creates REP socket server on a default port. Following request will be
    serviced:

    * Register publisher
    * Register subscriber
    * Find publisher
    * Find subscriber
    * Remove publisher
    * Remove subscriber
    """

    def __init__(self, fe_host="localhost"):
        """Constructor used by xMsgNode objects.

        xMsgRegistrar needs periodically report/update frontend registration
        database with data stored in its local databases. This process
        makes sure we have proper duplication of the registration data
        for clients seeking global discovery of publishers/subscribers.
        It is true that discovery can be done using xMsgRegistrar
        service only, however by introducing the fe_host, xMsgRegistrar
        can come and go, thus making xMsg message-space elastic.
        """
        self.context = zmq.Context()
        self.proxy = xMsgProxy(self.context)
        self.reg_service = xMsgRegService(self.context, fe_host)
        self.node = "frontend"

        if fe_host != "localhost":
            self.node = "local"

    def start(self):
        """Starts the registrar services"""
        self.reg_service.start()

        xMsgUtil.log("Local ip: %s" % xMsgUtil.get_local_ip())
        msg = ("xMsg %s registration and discovery server has started"
               % self.node)
        xMsgUtil.log(msg)

        try:
            self.proxy.start()
            self._join()

        except zmq.error.ZMQError:
            xMsgUtil.log("Cannot start proxy: address already in use...")
            self.shutdown()

    def shutdown(self):
        """Shutdowns the register and destroy the context"""
        xMsgUtil.log("xMsgRegistrar is being shutdown gracefully")
        # Kill the thread before terminating the context
        self.reg_service.stop()
        # Give it a little time before destroying the context
        xMsgUtil.sleep(1)
        # Now we destroy the shared context
        self.context.destroy()

    def _join(self):
        """Join method for the registration service"""
        self.reg_service.join()


def runner(fe_host="localhost"):
    try:
        registrar = xMsgRegistrar(fe_host)
        registrar.start()

    except KeyboardInterrupt:
        registrar.shutdown()
        return


def main():
    """Main function to start a xMsg registrar

    Usage:
    ::
        python xmsg/xsys/xMsgRegistrar.py

    *Or if you want to specify the frontend host:*
    ::
        python xmsg/xsys/xMsgRegistrar.py --fe_host <hostname>
    """
    if len(sys.argv) == 3:
        if str(sys.argv[1]) == "--fe_host":
            runner(sys.argv[2])

        else:
            print " Wrong option. Accepts --fe_host option only."
            return

    elif len(sys.argv) == 1:
        runner()

if __name__ == '__main__':
    main()
