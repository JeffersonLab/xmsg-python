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
import zmq
import sys

from xsys.regdis.xMsgRegService import xMsgRegService
from xsys.regdis.xMsgRegDriver import xMsgRegDriver
from xsys.xMsgProxy import xMsgProxy
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil


__author__ = 'gurjyan'


class xMsgRegistrar(xMsgRegDriver):
    """
    xMsgRegistrar

    The main registrar service, that always runs in a
    separate thread. Contains two separate databases
    to store publishers and subscribers registration data.
    The key for the data base is xMsg topic, constructed as:
    domain:subject:type
    Creates REP socket server on a default port
    Following request will be serviced:
     <ul>
           <li>Register publisher</li>
           <li>Register subscriber</li>
           <li>Find publisher</li>
           <li>Find subscriber</li>
     </ul>

    """

    context = str(xMsgConstants.UNDEFINED)

    def __init__(self, fe_host="localhost"):
        """
        Constructor used by xMsgNode objects.
        xMsgNode needs periodically report/update xMsgFe registration
        database with data stored in its local databases. This process
        makes sure we have proper duplication of the registration data
        for clients seeking global discovery of publishers/subscribers.
        It is true that discovery can be done using xMsgNode registrar
        service only, however by introducing xMsgFE, xMsgNodes can come
        and go, thus making xMsg message-space elastic.

        """
        xMsgRegDriver.__init__(self, zmq.Context() , fe_host)

        self.proxy = xMsgProxy(self.get_context())

        self.reg_service = xMsgRegService(self.get_context())
        self.reg_service.daemon = True
        self.reg_service.start()

        xMsgUtil.log("Info: xMsg local registration and discovery server is started")

        try:
            self.proxy.start()

        except:
            self.shutdown()

    def shutdown(self):
        xMsgUtil.log("xMsgRegistrar is being shutdown gracefully")
        self.get_context().destroy()

    def join(self):
        self.reg_service.join()


def main():
    if len(sys.argv) == 3:
        if str(sys.argv[0]) == "-fe_host":
            try:
                registrar = xMsgRegistrar(str(sys.argv[2]))
                registrar.join()

            except:
                registrar.shutdown()

        else:
            print " Wrong option. Accepts -fe_host option only."
            return
    elif len(sys.argv) == 1:
        try:
            registrar = xMsgRegistrar()
            registrar.join()

        except:
            registrar.shutdown()
            return

if __name__ == '__main__':
    main()
