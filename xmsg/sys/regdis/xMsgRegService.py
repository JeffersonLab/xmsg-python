# coding=utf-8

import threading
import zmq
from sets import Set

from xmsg.core.xMsgExceptions import AddressInUseException
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.sys.regdis.xMsgRegRequest import xMsgRegRequest
from xmsg.sys.regdis.xMsgRegResponse import xMsgRegResponse
from xmsg.sys.regdis.xMsgRegDatabase import xMsgRegDatabase


class xMsgRegService(threading.Thread):
    """The main registration service, that always runs in a separate thread.
    Contains two separate databases to store publishers and subscribers
    registration data.
    The key for the data base is xMsg topic, constructed as:

    *domain:subject:type*

    Creates REP socket server on a default port
    Following request will be serviced:

    * Register publisher
    * Register subscriber
    * Find publisher
    * Find subscriber
    * Remove publisher
    * Remove subscriber
    * Remove All registration

    Attributes:
        context (zmq.Context): zmq context
        host (String): registration service host
        port (int): registrar service port. By default is 8888
        subscribers_db (xMsgRegDatabase): subscribers database
        publishers_db (xMsgRegDatabase): publishers database
    """

    def __init__(self, context, reg_address):
        super(xMsgRegService, self).__init__()
        self.context = context
        self.address = reg_address.address

        # Thread settings
        self.daemon = True
        self._stop = threading.Event()

        # Databases for publishers and subscribers
        self.subscribers_db = xMsgRegDatabase()
        self.publishers_db = xMsgRegDatabase()

    def stop(self):
        self._stop.set()

    def stopped(self):
        self._stop.isSet()

    def run(self):
        """xMsgRegService thread method to process registration requests

        During its execution will receive the registration request and
        will process the petition, sending a response.

        Method description:
        ::
            while thread is alive:
                reg_service_response = process_request(registration_request)
                send_back(reg_service_response)

        """
        registrar_socket = None
        try:
            registrar_socket = self.context.socket(zmq.REP)
            registrar_socket.bind(self.address)
        except zmq.ZMQError:
            raise AddressInUseException("Registrar address already being used")

        else:
            while threading.currentThread().is_alive() and not self.stopped():
                try:
                    registrar_request = registrar_socket.recv_multipart()
                    if not registrar_request:
                        continue

                    response = self.process_request(registrar_request)
                    registrar_socket.send_multipart(response.msg())

                except zmq.error.ContextTerminated:
                    self.stop()
                    return

                except KeyboardInterrupt:
                    self.stop()
                    return

                except Exception as e:
                    self.stop()
                    xMsgUtil.log("xMsgRegService received: %s" % e)
                    return

    def process_request(self, registration_request):
        """Method to process the registration request and interact with the
        Registration DB

        The process_request method will receive a request from a xMsg actor
        to register or for obtaining registration info from the database.
        The method is able to respond to the following requests (this request
        is taken from the topic of the request message):

        * *REMOVE_ALL_REGISTRATION*
        * *REGISTER_PUBLISHER*
        * *REGISTER_SUBSCRIBER*
        * *REMOVE_PUBLISHER*
        * *REMOVE_SUBSCRIBER*
        * *FIND_PUBLISHER*
        * *FIND_SUBSCRIBER*
        * *REMOVE_ALL_REGISTRATION*

        Any other request, not listed among the previous request topics is
        considered unknown, and the method will return *xMsgContants.ERROR*

        Args:
            registration_request (bytes[]): Multipart message received by the
                xMsgRegService thread.

        Returns:
            xMsgResponse: response to the received registration request
        """
        try:
            request = xMsgRegRequest.create_from_multipart(registration_request)
            sender = "%s:%s" % (xMsgUtil.get_local_ip(),
                                xMsgConstants.REGISTRAR)
            registration = Set([])
            s_host = xMsgConstants.UNDEFINED

            msg = "Received a request from %s to %s" % (request.sender,
                                                        request.topic)
            xMsgUtil.log(msg)

            if request.topic == xMsgConstants.REMOVE_ALL_REGISTRATION:
                s_host = request.get_data().domain

            if request.topic == xMsgConstants.REGISTER_PUBLISHER:
                self.publishers_db.register(request.get_data())

            elif request.topic == xMsgConstants.REGISTER_SUBSCRIBER:
                self.subscribers_db.register(request.get_data())

            elif request.topic == xMsgConstants.REMOVE_PUBLISHER:
                self.publishers_db.remove(request.get_data())

            elif request.topic == xMsgConstants.REMOVE_SUBSCRIBER:
                self.subscribers_db.remove(request.get_data())

            elif request.topic == xMsgConstants.REMOVE_ALL_REGISTRATION:
                self.subscribers_db.remove_by_host(s_host)
                self.publishers_db.remove_by_host(s_host)

            elif request.topic == xMsgConstants.FIND_PUBLISHER:
                register = request.get_data()
                registration = self.publishers_db.find(register.domain,
                                                       register.subject,
                                                       register.type)

            elif request.topic == xMsgConstants.FIND_SUBSCRIBER:
                register = request.get_data()
                registration = self.subscribers_db.find(register.domain,
                                                        register.subject,
                                                        register.type)

            else:
                xMsgUtil.log("Warning: unknown registration request type...")
                xMsgUtil.log("Warning: got message %s" % request.topic)
                registration = xMsgConstants.ERROR
            # send a response to request
            return xMsgRegResponse(request.topic, sender, registration)

        except zmq.error.ContextTerminated:
            xMsgUtil.log("xMsgRegService: Context terminated")
            return
