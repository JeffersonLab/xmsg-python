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
import signal
import zmq
from multiprocessing import Pool

from xmsg.core.xMsgExceptions import NullConnection, NullMessage
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data import xMsgRegistration_pb2
from xmsg.net.xMsgConnection import xMsgConnection
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver


__author__ = 'gurjyan'


class xMsg(object):
    """xMsg base class that provides methods for organizing pub/sub communications

    This class provides a local database of xMsgCommunication for publishing
    and/or subscribing messages without requesting registration information
    from the local (running within xMsgRegistrar) and/or global registrar
    services.

    This class also provides a thread pool for servicing received messages
    (as a result of a subscription) in separate threads.

    Attributes:
        myname (String): name of the xMsg actor instance
        driver (xMsgRegDriver): registration driver
        context (zmq.Context): communication context for the instance
        pool_size (int): fixed size thread pool
    """

    def __init__(self, name, fe_host, **kwargs):
        """xMsg Constructor

        Constructor, requires the name of the FrontEnd host that is used to
        create to the registrar service running within the xMsgFE.
        Creates the zmq context object and thread pool for servicing received
        messages in a separate threads.

        Args:
            name (String): name of the xMsg actor instance
            fe_host (String): hostname of the frontend host

        Keyword arguments:
            pool_size (int): size of the actors thread pool
            context (zmq.Context): communication context

        Returns:
            xMsg: xmsg object
        """
        # Name of xMsg Actor
        self.myname = name

        context = kwargs.pop("context", False)
        self.context = context if context else zmq.Context()

        pool_size = kwargs.pop("pool_size", False)
        self.pool_size = pool_size if pool_size else 2

        # Initialize registration driver
        self.driver = xMsgRegDriver(self.context, fe_host)
        self.localhost_ip = xMsgUtil.host_to_ip("localhost")

        # create fixed size thread pool
        self._thread_pool = Pool(self.pool_size, self.__init_worker)

        # Private db of stored connections
        self._connections = dict()

    def connect(self, address):
        """Connects to the node by creating two sockets for publishing and
        subscribing/receiving messages.

        It returns and the same time stores in the local connection database
        created xMsgConnection object.

        Args:
            address (xMsgAddress): xmsg address object

        Returns:
            xMsgConnection: xmsg connection object
        """

        # First check to see if we have already
        # established connection to this address
        if address.get_key in self._connections.keys():
            return self._connections.get(address.get_key())
        else:
            # Otherwise create sockets to the
            # requested address, and store the created
            # connection object for the future use.
            # Return the reference to the connection object
            fe_connection = xMsgConnection()
            fe_connection.set_address(address)
            host = address.get_host()
            port = address.get_port()
            connect = str(xMsgConstants.CONNECT)

            pub_socket = self.driver.zmq_socket(self.context, zmq.PUB,
                                                host, port, connect)
            fe_connection.set_pub_sock(pub_socket)

            sub_socket = self.driver.zmq_socket(self.context, zmq.SUB,
                                                host, port + 1, connect)
            fe_connection.set_sub_sock(sub_socket)

            self._connections[address.get_key()] = fe_connection
            return fe_connection

    def destroy(self, linger=-1):
        """ Destroys the created context and terminates the thread pool.

        Args:
            linger (int): milliseconds that the thread will try to send
                messages after the socket has been closed.Default value
                is -1, which in ZMQ means to linger forever.
        """
        self.context.destroy(linger)
        self.__terminate_threadpool()

    def get_new_connection(self, address):
        """Returns a new xMsgConnection object to the xMsg proxy, using
        new zmq context

        Args:
            address (xMsgAddress): xMsg address object

        Returns:
            feCon (xMsgConnection): xMsg connection object
        """
        new_context = zmq.Context()
        feCon = xMsgConnection()
        feCon.set_address(address)
        soc_p = self.driver.zmq_socket(new_context,
                                       zmq.PUB,
                                       address.get_host(),
                                       address.get_port(),
                                       str(xMsgConstants.CONNECT))
        feCon.set_pub_sock(soc_p)

        soc_s = self.driver.zmq_socket(new_context,
                                       zmq.SUB,
                                       address.get_host(),
                                       address.get_port() + 1,
                                       str(xMsgConstants.CONNECT))
        feCon.set_sub_sock(soc_s)
        return feCon

    def register_publisher(self, topic,
                           description=str(xMsgConstants.UNDEFINED)):
        """Registers xMsg publisher actor in the publishers database

        If you are periodically publishing data, use this method to
        register yourself as a publisher with the local registrar.
        This is necessary for future subscribers to discover and
        listen to your messages.

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): publisher description string
        """
        r_data = self._registration_builder(topic, description, True)

        self.driver.register_local(self.myname, r_data, True)

    def register_subscriber(self, topic,
                            description=str(xMsgConstants.UNDEFINED)):
        """Subscribers xMsg publisher actor in the subscribers database

        If you are a subscriber and want to listen messages on a specific
        topic from a future publishers, you should register yourself as
        a subscriber with the local registrar.

        Future publishers might express an interest to publish data to a
        a required topic of interest or might publish data only if there
        are active listeners/subscribers to their published topic.

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): subscriber description string
        """
        r_data = self._registration_builder(topic, description, False)

        self.driver.register_local(self.myname, r_data, False)

    def remove_publisher_registration(self, topic):
        """Removes publisher registration both from the local and then from the
        global registration databases

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
        """
        r_data = self._registration_builder(topic, None, True)

        self.driver.remove_registration_local(self.myname, r_data, True)
        self.driver.remove_registration_fe(self.myname, r_data, True)

    def remove_subscriber_registration(self, topic):
        """Removes subscriber registration both from the local and then from the
        global registration databases

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
        """
        r_data = self._registration_builder(topic, None, False)

        self.driver.remove_registration_local(self.myname, r_data, False)
        self.driver.remove_registration_fe(self.myname, r_data, False)

    def find_local_publisher(self, topic,
                             description=str(xMsgConstants.UNDEFINED)):
        """Finds all local publishers, publishing  to a specified topic

        Note: xMsg defines a topic as domain:subject:type

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): publisher description string

        Returns:
            xMsgRegistration: registration info object
        """
        r_data = self._registration_builder(topic, description, True)

        return self.driver.find_local(self.myname, r_data, True)

    def find_local_subscriber(self, topic,
                              description=str(xMsgConstants.UNDEFINED)):
        """Finds all local subscribers, subscribing  to a specified topic

        Note: xMsg defines a topic as domain:subject:type

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): subscriber description string

        Returns:
            list: list of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, False)

        return self.driver.find_local(self.myname, r_data, False)

    def find_publisher(self, topic,
                       description=str(xMsgConstants.UNDEFINED)):
        """
        Finds all publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): subscriber description string

        Returns:
            list: list of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, True)

        return self.driver.find_global(self.myname, r_data, True)

    def find_subscriber(self, topic,
                        description=str(xMsgConstants.UNDEFINED)):
        """
        Finds all subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): subscriber description string

        Returns:
            list: list of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, False)

        return self.find_global(self.myname, r_data, False)

    def publish(self, connection, transient_message):
        """Publishes data to a specified xMsg topic.

        3 elements are defining xMsg topic: domain:subject:tip
        Topic is obtained in xMsgMessage.get_topic() method.
        If subject is set "*" type will be ignored. Here are examples of
        accepted topic definitions:

        * domain:*:*
        * domain:subject:*
        * domain:subject:type

        This method will perform input data, i.e. xMsgMessage object
        serialization.

        Args:
            connection (xMsgConnection): object
            transient_message (xMsgMessage): transient data object

        Raises:
            NullConnection: if there is no connection object
            NullMessage: if there is no message object
        """
        con = connection.get_pub_sock()

        # Check connection
        if not con:
            raise NullConnection("xMsg: Null connection object")
        # Check msg
        if not transient_message:
            raise NullMessage("xMsg: Null message object")

        con.send_multipart(transient_message.serialize())

    def subscribe(self, connection, topic, callback_function, is_sync):
        """Subscribes to a specified xMsg topic.

        3 elements are defining xMsg topic: domain:subject:tip
        Topic is constructed from these elements separated by ":"
        Domain is required , however subject and topic can be set to "*".
        If subject is set "*" type will be ignored. Here are examples of
        accepted topic definitions:

        * domain:*:*
        * domain:subject:*
        * domain:subject:tip

        Supplied user callback must be defined by the user.
        This method will de-serialize received xMsgData object and pass it
        to the user implemented callback method.
        In the case is_sync input parameter is set to be false the method will
        utilize private thread pool to run user callback method in a separate
        thread.

        Args:
            connection (xMsgConnection):  connection object

            callback_function: user supplied callback function
            is_sync (bool): if set to true method will block until user
                callback method is returned. In case you need to run in a
                multi-threaded mode, i.e. running parallel user call backs,
                is_sync = False
        """
        subscriber_thread = threading.Thread(target=self.__sub_module,
                                             args=(connection,
                                                   topic,
                                                   callback_function,
                                                   is_sync))
        subscriber_thread.setDaemon(True)
        subscriber_thread.start()

    def __sub_module(self, connection, topic, callback_function, is_sync):
        # get subscribers socket connection
        con = connection.get_sub_sock()

        # subscribe to the topic
        con.setsockopt(zmq.SUBSCRIBE, str(topic))

        # wait for messages published to a required topic
        while True:
            try:
                response = con.recv_multipart()

                if len(response) == 3:
                    serialized_data = response[2]
                    transient_message = xMsgMessage(topic, serialized_data)

                    if is_sync:
                        callback_function(transient_message)

                    else:
                        sub_thread = threading.Thread(target=callback_function,
                                                      args=[transient_message])
                        sub_thread.daemon = True
                        sub_thread.start()

            except KeyboardInterrupt, zmq.error.ContextTerminated:
                self.destroy()
                return

            except:
                return

    def _registration_builder(self, topic, description, publisher=True):
        """Creates a xMsgRegistration object

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
            description (String): subscriber description string
            publisher (bool): Is publisher flag, if it is set to True the
                registration object generated corresponds to a publisher,
                otherwise corresponds to a subscriber.
        """
        r_data = xMsgRegistration_pb2.xMsgRegistration()
        r_data.name = self.myname
        if description:
            r_data.description = description
        r_data.host = xMsgUtil.host_to_ip(self.localhost_ip)
        r_data.port = int(xMsgConstants.DEFAULT_PORT)
        r_data.domain = topic.domain()
        r_data.subject = topic.subject()
        r_data.type = topic.type()

        if publisher:
            r_data.ownerType = xMsgRegistration_pb2.xMsgRegistration.PUBLISHER
        else:
            r_data.ownerType = xMsgRegistration_pb2.xMsgRegistration.SUBSCRIBER

        return r_data

    def get_pool_size(self):
        """Returns internal thread pool size

        Returns:
            pool_size (int): Size of the thread pool
        """
        return self.pool_size

    def __init_worker(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def __terminate_threadpool(self):
        """Terminates the xMsg threadpool"""
        self._thread_pool.terminate()
        self._thread_pool.join()
