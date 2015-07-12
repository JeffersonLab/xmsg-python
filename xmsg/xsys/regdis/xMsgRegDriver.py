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

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgExceptions import TimeoutReached, RegistrationException
from xmsg.xsys.regdis.xMsgRegResponse import xMsgRegResponse
from xmsg.xsys.regdis.xMsgRegRequest import xMsgRegRequest

__author__ = 'gurjyan'


class xMsgRegDriver:

    # Front-end registrar server (req/rep) connection socket
    _feConnection = str(xMsgConstants.UNDEFINED)

    # Local registrar server (req/rep) connection socket
    _lnConnection = str(xMsgConstants.UNDEFINED)

    # zmq context
    context = str(xMsgConstants.UNDEFINED)

    def __init__(self, context, fe_host="localhost"):
        self.context = context

        self._feConnection = self.zmq_socket(self.context, zmq.REQ,
                                             xMsgUtil.host_to_ip(fe_host),
                                             int(xMsgConstants.REGISTRAR_PORT),
                                             str(xMsgConstants.CONNECT))
        if fe_host != "localhost":
            self._lnConnection = self.zmq_socket(self.context, zmq.REQ,
                                                 xMsgUtil.host_to_ip("localhost"),
                                                 int(xMsgConstants.REGISTRAR_PORT),
                                                 str(xMsgConstants.CONNECT))
        else:
            self._lnConnection = self._feConnection

    def get_context(self):
        """
        Returns the main zmq socket context
        :return zmq context
        """
        return self.context

    def _register(self, conn_socket, name, data, is_publisher):
        """
        Sends registration request to the server. Request is wired using
        xMsg message construct, that have 3 part: topic, sender, and data.
        Data is the object of the xMsgRegistrationData
        :param _connectionSocket connection socket defines the local or
                                front-end registration server
        :param name the name of the sender
        :param data xMsgRegistrationData object
        :param isPublisher if set to be true then this is a request to register
                           a publisher, otherwise this is a subscriber
                           registration request
        """
        # Data serialization
        if data.IsInitialized():
            dt = data.SerializeToString()

            # Send topic, sender, followed by the data
            # Topic of the message is a string = "registerPublisher"
            # or "registerSubscriber"
            if is_publisher:
                topic = str(xMsgConstants.REGISTER_PUBLISHER)
            else:
                topic = str(xMsgConstants.REGISTER_SUBSCRIBER)
            timeout = int(xMsgConstants.REGISTER_REQUEST_TIMEOUT)
            request = xMsgRegRequest(topic, name, dt)
            self.request(conn_socket, request, timeout)

    def _remove_registration(self, conn_socket, name, data, is_publisher):
        """
        Sends remove registration request to the server. Request is wired using
        xMsg message construct, that have 3 part: topic, sender, and data.
        Data is the object of the xMsgRegistrationData
        :param _connectionSocket connection socket defines the local or
                                front-end registration server
        :param name the name of the sender
        :param data xMsgRegistrationData object
        :param isPublisher if set to be true then this is a request to register
                          a publisher, otherwise this is a subscriber
                          registration request
        """

        # Data serialization
        if data.IsInitialized():
            dt = data.SerializeToString()

            # Send topic, sender, followed by the data
            # Topic of the message is a string = "removePublisher"
            # or "removeSubscriber"

            if is_publisher:
                topic = str(xMsgConstants.REMOVE_PUBLISHER)
            else:
                topic = str(xMsgConstants.REMOVE_SUBSCRIBER)
            timeout = int(xMsgConstants.REGISTER_REQUEST_TIMEOUT)
            request = xMsgRegRequest(topic, name, dt)
            self.request(conn_socket, request, timeout)

    def remove_all_registration_fe(self, host, name):
        """
        Removes all xMsg actors (publishers and subscribers) registration from
        the front-end global registration and discovery database that were
        previously registered on a specified host local database. This method
        is usually called by the xMsgNode Registrar when it shuts down or gets
        interrupted.
        :param host: host name of the xMsgNode
        :param name: the name of the sender
        """

        # topic
        topic = str(xMsgConstants.REMOVE_ALL_REGISTRATION)
        timeout = int(xMsgConstants.REGISTER_REQUEST_TIMEOUT)
        request = xMsgRegRequest(topic, name, host)
        self.request(self._feConnection, request, timeout)

    def _find(self, conn_socket, name, data, is_publisher):
        """
        Searches registration database (local or global), defined by the
        connection socket object, for the publisher or subscriber based
        on the xMsg topic components. xMsg topic components, i.e. domain,
        subject and types are defined within the xMsgRegistrationData object.

        :param connectionSocket: connection socket defines the local or
                                 front-end registration server
        :param name: the name of the sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to find
                            publishers, otherwise subscribers
        :return: List of publishers or subscribers xMsgRegistrationData objects
                 that publish/subscribe required topic

        """
        # Data serialization
        if data.IsInitialized():
            serialized_data = data.SerializeToString()

            # Send topic, sender, followed by the data
            # Topic of the message is a string = "findPublisher"
            # or "findSubscriber"
            if is_publisher:
                topic = str(xMsgConstants.FIND_PUBLISHER)
            else:
                topic = str(xMsgConstants.FIND_SUBSCRIBER)
            timeout = int(xMsgConstants.FIND_REQUEST_TIMEOUT)
            request_message = xMsgRegRequest(topic, name, serialized_data)
            return self.request(conn_socket, request_message, timeout)
            

    def register_fe(self, name, data, is_publisher):
        """
        Registers xMsg actor with the front-end registration and discovery
        server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._register(self._feConnection, name, data, is_publisher)

    def register_local(self, name, data, is_publisher):
        """
        Registers xMsg actor with the local registration and discovery server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._register(self._lnConnection, name, data, is_publisher)

    def remove_registration_fe(self, name, data, is_publisher):
        """
        Removes xMsg actor from the front-end registration and discovery server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._remove_registration(self._feConnection, name, data, is_publisher)

    def remove_registration_local(self, name, data, is_publisher):
        """
        Removes xMsg actor from the local registration and discovery server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._remove_registration(self._lnConnection, name, data, is_publisher)

    def find_local(self, name, data, is_publisher):
        """
        Searches the local registration and discovery databases for an actor
        that publishes or subscribes the topic of the interest.
        The search criteria i.e. topic is defined within the
        xMsgRegistrationData object.
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        :return List of xMsgRegistrationData objects
        """
        return self._find(self._lnConnection, name, data, is_publisher)

    def find_global(self, name, data, is_publisher):
        """
        Searches the FE registration and discovery databases for an actor
        that publishes or subscribes the topic of the interest.
        The search criteria i.e. topic is defined within the
        xMsgRegistrationData object.
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        :return List of xMsgRegistrationData objects
        """
        return self._find(self._feConnection, name, data, is_publisher)
    
    def request(self, socket, request, timeout):
        request_msg = request.get_serialized_msg()
        try:
            socket.send_multipart(request_msg)
        except:
            raise RegistrationException("Error sending registration message")
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        if poller.poll(timeout * 1000):
            # timeout in milliseconds
            request = socket.recv_multipart()
            response = xMsgRegResponse.create_from_multipart_request(request)

            if response.get_status() != str(xMsgConstants.SUCCESS):
                raise RegistrationException(response.get_status())

            xMsgUtil.log("Info: xMsg actor has been registered in node")
            return response.get_data()
        else:
            raise TimeoutReached("Timeout processing registration request")

    def zmq_socket(self, context, socket_type, h, port, boc):
        """
        Creates and returns zmq socket object

        :param context zmq context
        :param socket_type the type of the socket (integer defined by zmq)
        :param h host name
        :param port port number
        :param boc if set 0 socket will be bind, otherwise it will connect.
                    Note that for xMsg proxies we always connect (boc = 1)
                     (proxies are XPUB/XSUB sockets).
        :return zmq socket object
        """
        # Create a zmq socket
        sb = context.socket(socket_type)
        if socket_type == zmq.REQ:
            sb.setsockopt(zmq.LINGER, 0)

        if boc == str(xMsgConstants.BIND):
            # Bind socket to the host and port
            sb.bind("tcp://%s:%s" % (str(h), str(port)))
        elif boc == str(xMsgConstants.CONNECT):

            # Connect to the host and port
            sb.connect("tcp://%s:%s" % (str(h), str(port)))
        return sb
