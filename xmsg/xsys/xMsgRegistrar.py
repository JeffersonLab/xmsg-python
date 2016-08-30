# coding=utf-8

import zmq

from xmsg.xsys.regdis.xMsgRegService import xMsgRegService
from xmsg.xsys.xMsgProxy import xMsgProxy
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
        self.proxy = xMsgProxy(self.context)
        self.reg_service = xMsgRegService(self.context, RegAddress("localhost"))
        self.node = "local"

    def start(self):
        try:
            """Starts the registrar services"""
            self.reg_service.start()

            xMsgUtil.log("Local ip: %s" % xMsgUtil.get_local_ip())
            msg = ("xMsg %s registration and discovery server has started"
                   % self.node)
            xMsgUtil.log(msg)
            self.proxy.start()
            self._join()

        except zmq.error.ZMQError:
            xMsgUtil.log("Cannot start node: address already in use...")
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


def main():
    """Main function to start a xMsg registrar

    Usage:
    ::
        python xmsg/xsys/xMsgRegistrar.py
    """
    try:
        registrar = xMsgRegistrar()
        registrar.start()

    except KeyboardInterrupt:
        registrar.shutdown()
        return

    except zmq.error.ZMQError:
        xMsgUtil.log("Cannot start registrar: address already in use...")
        return -1

if __name__ == '__main__':
    main()
