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

import threading
import zmq
from sets import Set

from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.xsys.regdis.xMsgRegUpdater import xMsgRegUpdater
from xmsg.xsys.regdis.xMsgRegRequest import xMsgRegRequest
from xmsg.xsys.regdis.xMsgRegResponse import xMsgRegResponse
from xmsg.xsys.regdis.xMsgRegDatabase import xMsgRegDatabase
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver


class xMsgRegService(threading.Thread):
    '''
    The main registration service, that always runs in a separate thread.
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
    '''

    def __init__(self, context, fe_host):
        super(xMsgRegService, self).__init__()
        self.context = context
        self.host = str(xMsgConstants.ANY)
        self.port = int(xMsgConstants.REGISTRAR_PORT)
        self.daemon = True

        # Databases for publishers and subscribers
        self.subscribers_db = xMsgRegDatabase()
        self.publishers_db = xMsgRegDatabase()

        if fe_host != "localhost":
            # Launching the frontend updater
            self.driver = xMsgRegDriver(context, fe_host)
            self.updater = xMsgRegUpdater(self.driver,
                                          self.publishers_db,
                                          self.subscribers_db)
            self.updater.start()

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
        reg_service_socket = self.context.socket(zmq.REP)
        reg_service_socket.bind("tcp://%s:%d" % (self.host, self.port))

        while True and threading.currentThread().is_alive():
            try:
                registration_request = reg_service_socket.recv_multipart()
                if not registration_request:
                    continue
                reg_service_response = self.process_request(registration_request)
                reg_service_socket.send_multipart(reg_service_response.get_serialized_msg())
                del registration_request
                del reg_service_response

            except zmq.error.ContextTerminated:
                self._log("Context terminated at xMsgRegistrationService")
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
            request = xMsgRegRequest.create_from_multipart_request(registration_request)
            registration = Set([])
            sender = "%s:%s" % (xMsgUtil.get_local_ip(),
                                str(xMsgConstants.REGISTRAR))

            msg = "Received a request from %s to %s" % (request.get_sender(),
                                                        request.get_topic())
            self._log(msg)

            s_host = str(xMsgConstants.UNDEFINED)

            if request.get_topic() == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                s_host = request.get_data().domain

            if request.get_topic() == str(xMsgConstants.REGISTER_PUBLISHER):
                self.publishers_db.register(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REGISTER_SUBSCRIBER):
                self.subscribers_db.register(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REMOVE_PUBLISHER):
                self.publishers_db.remove(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REMOVE_SUBSCRIBER):
                self.subscribers_db.remove(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                self.subscribers_db.remove_by_host(s_host)
                self.publishers_db.remove_by_host(s_host)

            elif request.get_topic() == str(xMsgConstants.FIND_PUBLISHER):
                register = request.get_data()
                registration = self.publishers_db.find(register.domain,
                                                       register.subject,
                                                       register.type)
                self._log("RegService has found: %d publishers" % len(registration))

            elif request.get_topic() == str(xMsgConstants.FIND_SUBSCRIBER):
                register = request.get_data()
                registration = self.subscribers_db.find(register.domain,
                                                        register.subject,
                                                        register.type)
                self._log("RegService has found: %d subscribers" % len(registration))

            else:
                self._log("Warning: unknown registration request type...")
                self._log("Warning: got message %s" % request.get_topic())
                registration = str(xMsgConstants.ERROR)
            # send a response to request
            return xMsgRegResponse(request.get_topic(), sender, registration)

        except zmq.error.ContextTerminated:
            self._log("Context terminated at xMsgRegService")
            return

    def _log(self, message):
        """Prints output from xMsgRegService with a time stamp

        Args:
            message (String): message to log
        """
        # Logging behavior should be defined
        # Meaning storing messages or notifying to someone about the Event
        print "%s %s" % (xMsgUtil.current_time(), message)
