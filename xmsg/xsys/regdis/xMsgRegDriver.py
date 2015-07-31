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

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgExceptions import TimeoutReached, RegistrationException
from xmsg.xsys.regdis.xMsgRegResponse import xMsgRegResponse
from xmsg.xsys.regdis.xMsgRegRequest import xMsgRegRequest

__author__ = 'gurjyan'


class xMsgRegDriver:
    """Methods for registration and discovery of xMsg actors, i.e. publishers
    and subscribers.

    This class also contains the base method used by all xMsg extending classes
    to create 0MQ socket for communications. This means that this class owns
    the 0MQ context.
    The sockets use the default registrar port: xMsgConstants#REGISTRAR_PORT.

    Attributes:
        context (zmq.Context): zmq context
        fe_host (String): xmsg frontend hostname
    """

    def __init__(self, context, fe_host="localhost"):
        # 0MQ context
        self.context = context

        # Connection settings
        fe_host_ip = xMsgUtil.host_to_ip(fe_host)
        localhost_ip = xMsgUtil.host_to_ip("localhost")
        registrar_port = int(xMsgConstants.REGISTRAR_PORT)
        connect = str(xMsgConstants.CONNECT)

        # Front-end registrar server (req/rep) connection socket
        self._feConnection = self.zmq_socket(self.context, zmq.REQ,
                                             fe_host_ip, registrar_port,
                                             connect)
        if fe_host != "localhost":
            # Local registrar server (req/rep) connection socket
            self._lnConnection = self.zmq_socket(self.context, zmq.REQ,
                                                 localhost_ip, registrar_port,
                                                 connect)
        else:
            self._lnConnection = self._feConnection

    def get_context(self):
        """Returns the main zmq socket context

        Returns:
            zmq.Context: zmq context
        """
        return self.context

    def _register(self, conn_socket, name, registration_data, is_publisher):
        """Sends registration request to the server

        Request is wired using xMsg message construct, that have 3 parts:
            topic, sender, and data.
        Data is the object of the xMsgRegistration

        Args:
            conn_socket (zmq.Socket):connection socket defines the local or
                front-end registration server
            name (String): the name of the sender
            data (xMsgRegistration): registration information object
            is_publisher (bool): if set to be true then this is a request
                to register a publisher, otherwise this is a subscriber
                registration request
        """
        # Data serialization
        if registration_data.IsInitialized():
            registration_data = registration_data.SerializeToString()
            # Send topic, sender, followed by the data
            # Topic of the message is a string = "registerPublisher"
            # or "registerSubscriber"
            if is_publisher:
                topic = str(xMsgConstants.REGISTER_PUBLISHER)

            else:
                topic = str(xMsgConstants.REGISTER_SUBSCRIBER)

            timeout = int(xMsgConstants.REGISTER_REQUEST_TIMEOUT)
            request = xMsgRegRequest(topic, name, registration_data)

            self._request(conn_socket, request, timeout)

    def _remove_registration(self, conn_socket, name, registration_data,
                             is_publisher):
        """Sends remove registration request to the server.

        Request is wired using xMsg message construct, that have 3 parts:
        topic, sender, and data. Data is the object of the xMsgRegistration

        Args:
            conn_socket (zmq.Socket): connection socket defines the local or
                front-end registration server
            name (String):the name of the sender
            registration_data (xMsgRegistration): registration information
                object
            is_publisher (bool): if set to be true then this is a request
                to register a publisher, otherwise this is a subscriber
                registration request
        """

        # Data serialization
        if registration_data.IsInitialized():
            serialized_data = registration_data.SerializeToString()
            # Send topic, sender, followed by the data
            # Topic of the message is a string = "removePublisher"
            # or "removeSubscriber"
            if is_publisher:
                topic = str(xMsgConstants.REMOVE_PUBLISHER)

            else:
                topic = str(xMsgConstants.REMOVE_SUBSCRIBER)

            timeout = int(xMsgConstants.REGISTER_REQUEST_TIMEOUT)
            request = xMsgRegRequest(topic, name, serialized_data)

            self._request(conn_socket, request, timeout)

    def remove_all_registration_fe(self, host, name):
        """Removes all xMsg actors registration from the front-end registration

        Removes all xMsg actors (publishers and subscribers) registration from
        the front-end global registration and discovery database that were
        previously registered on a specified host local database. This method
        is usually called by the xMsgRegistrar when it shuts down or gets
        interrupted.

        Args:
            host (String): host name of the xMsgNode
            name (String): the name of the sender
        """

        # topic
        topic = str(xMsgConstants.REMOVE_ALL_REGISTRATION)
        timeout = int(xMsgConstants.REGISTER_REQUEST_TIMEOUT)
        request = xMsgRegRequest(topic, name, host)

        self._request(self._feConnection, request, timeout)

    def _find(self, conn_socket, name, registration_data, is_publisher):
        """Find specific registration from local and global database

        Searches in the registration database (local or global), defined by the
        connection socket object, for the publisher or subscriber based
        on the xMsgTopic components. xMsgTopic components, i.e. domain,
        subject and types are defined within the xMsgRegistration object.

        Args:
            conn_socket (zmq.Socket): connection socket defines the local or
                front-end registration server
            name (String): the name of the sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher: if set to be true then this is a request to find
                publishers, otherwise subscribers

        Returns:
            list: list of publishers or subscribers xMsgRegistration objects
                that publish/subscribe required topic

        """
        # Data serialization
        if registration_data.IsInitialized():
            serialized_data = registration_data.SerializeToString()
            # Send topic, sender, followed by the data
            # Topic of the message is a string = "findPublisher"
            # or "findSubscriber"
            if is_publisher:
                topic = str(xMsgConstants.FIND_PUBLISHER)

            else:
                topic = str(xMsgConstants.FIND_SUBSCRIBER)

            timeout = int(xMsgConstants.FIND_REQUEST_TIMEOUT)
            request_message = xMsgRegRequest(topic, name, serialized_data)

            return self._request(conn_socket, request_message, timeout)

    def register_fe(self, name, registration_data, is_publisher):
        """Registers xMsg actor in front-end registration and discovery server

        Args:
            name (String): the name of the requester/sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher (bool): if set to be true then this is a request to
                register a publisher, otherwise this is a subscriber
                registration request
        """
        print "Me llamaron...."
        self._register(self._feConnection, name, registration_data,
                       is_publisher)

    def register_local(self, name, data, is_publisher):
        """Registers xMsg actor with the local registration and discovery server

        Args:
            name (String): the name of the requester/sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher (bool): if set to be true then this is a request to
                register a publisher, otherwise this is a subscriber
                registration request
        """
        self._register(self._lnConnection, name, data, is_publisher)

    def remove_registration_fe(self, name, data, is_publisher):
        """Removes xMsg actor from the front-end registration and discovery server

        Args:
            name (String): the name of the requester/sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher (bool): if set to be true then this is a request to
                register a publisher, otherwise this is a subscriber
                registration request
        """
        self._remove_registration(self._feConnection, name, data, is_publisher)

    def remove_registration_local(self, name, data, is_publisher):
        """Removes xMsg actor from the local registration and discovery server

        Args:
            name (String): the name of the requester/sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher (bool): if set to be true then this is a request to
                register a publisher, otherwise this is a subscriber
                registration request
        """
        self._remove_registration(self._lnConnection, name, data, is_publisher)

    def find_local(self, name, registration_data, is_publisher):
        """Searches the local registration and discovery databases for an actor

        The method will search for xMsg actors that publishes or subscribes
        the topic of the interest (locally). The search criteria i.e. topic is
        defined within the xMsgRegistration object.

        Args:
            name (String): the name of the requester/sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher: if set to be true then this is a request to
                register a publisher, otherwise this is a subscriber
                registration request

        Returns:
            list: list of xMsgRegistrationData objects
        """
        return self._find(self._lnConnection, name, registration_data,
                          is_publisher)

    def find_global(self, name, data, is_publisher):
        """Searches the FE registration and discovery databases for an actor

        The method will search for xMsg actors that publishes or subscribes
        the topic of the interest (globally). The search criteria i.e. topic is
        defined within the xMsgRegistrationData object.

        Args:
            name (String): the name of the requester/sender
            registration_data (xMsgRegistration): xMsgRegistration object
            is_publisher (bool): if set to be true then this is a request to
                register a publisher, otherwise this is a subscriber
                registration request

        Returns:
            list: list of xMsgRegistration objects
        """
        return self._find(self._feConnection, name, data, is_publisher)

    def _request(self, socket, request, timeout):
        """Sends a request to the given registrar server and waits the response.

        Args:
            socket (zmq.Socket): zmq socket for communication
            request (xMsgRegRequest): xMsg request object
            timeout (int): timeout for processing request in seconds

        Returns:
            bytes[]: serialized registration information
        """
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

    def zmq_socket(self, context, socket_type, hostname, port, boc):
        """Creates and returns zmq socket object

        Args:
            context (zmq.Context): zmq context
            socket_type (int): the type of the socket (integer defined by zmq)
            hostname (String): host name
            port (int): port number
            boc (String): 'bind' or 'connect' host and port to socket
                Note that for xMsg proxies we always connect (boc = 'connect')
                (proxies are XPUB/XSUB sockets).

        Returns:
            zmq.Socket: zmq socket object
        """
        # Create a zmq socket
        sb = context.socket(socket_type)
        sb.set_hwm(0)

        if boc == str(xMsgConstants.BIND):
            # Bind socket to the host and port
            sb.bind("tcp://%s:%s" % (str(hostname), str(port)))

        elif boc == str(xMsgConstants.CONNECT):
            # Connect to the host and port
            sb.connect("tcp://%s:%s" % (str(hostname), str(port)))

        return sb
