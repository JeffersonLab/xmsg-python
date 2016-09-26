# coding=utf-8

import zmq

from xmsg.core.xMsgExceptions import AddressInUseException
from xmsg.sys.regdis.xMsgRegService import xMsgRegService
from xmsg.sys.xMsgProxy import xMsgProxy
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.net.xMsgAddress import RegAddress


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

    def __init__(self):
        """Constructor used by xMsgNode objects.

        xMsgRegistrar needs periodically report/update frontend registration
        database with data stored in its local databases. This process
        makes sure we have proper duplication of the registration data
        for clients seeking global discovery of publishers/subscribers.
        It is true that discovery can be done using xMsgRegistrar
        service only, however by introducing the fe_host, xMsgRegistrar
        can come and go, thus making xMsg message-space elastic.
        """
        self.context = zmq.Context.instance()
        self.proxy = xMsgProxy(self.context, "localhost", 7771)
        self.reg_service = xMsgRegService(self.context, RegAddress())

    def start(self):
        try:
            """Starts the registrar services"""
            self.reg_service.start()

            xMsgUtil.log("Local ip: %s" % xMsgUtil.get_local_ip())
            xMsgUtil.log("Local registration and discovery server started")
            self.proxy.start()
            self.reg_service.join()

        except AddressInUseException as e:
            xMsgUtil.log(e.message)
            self.shutdown()

    def shutdown(self):
        """Shutdowns the register and destroy the context"""
        xMsgUtil.log("xMsgRegistrar is being shutdown gracefully")
        # Kill the thread before terminating the context


def main():
    """Main function to start a xMsg registrar

    Usage:
    ::
        python xmsg/sys/xMsgRegistrar.py
    """
    registrar = xMsgRegistrar()
    registrar.start()


if __name__ == '__main__':
    main()
