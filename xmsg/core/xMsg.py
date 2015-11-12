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

import signal
import zmq
from random import randint
from multiprocessing import Pool

from xmsg.core.xMsgExceptions import NullConnection, NullMessage
from xmsg.core.xMsgSubscription import xMsgSubscription
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data import xMsgRegistration_pb2
from xmsg.net.xMsgConnectionSetup import xMsgConnectionSetup
from xmsg.net.xMsgConnection import xMsgConnection
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver


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

    def __init__(self, name, proxy_address=ProxyAddress(),
                 registrar_address=RegAddress(), **kwargs):
        """xMsg Constructor

        Constructor, requires the name of the FrontEnd host that is used to
        create to the registrar service running within the xMsgFE.
        Creates the zmq context object and thread pool for servicing received
        messages in a separate threads.

        Args:
            name (String): name of the xMsg actor instance
            local_address (String): local hostname
            frontend_address (String): frontend hostname

        Keyword arguments:
            pool_size (int): size of the actors thread pool
            context (zmq.Context): communication context

        Returns:
            xMsg: xmsg object
        """
        # Name of xMsg Actor
        self.myname = name

        context = kwargs.pop("context", False)
        self.context = context or zmq.Context.instance()

        pool_size = kwargs.pop("pool_size", False)
        self.pool_size = pool_size or 2

        self.default_proxy_address = proxy_address
        self.default_registrar_address = registrar_address

        # Initialize registration driver
        self.driver = xMsgRegDriver(self.context, registrar_address)

        # create fixed size thread pool
        self._thread_pool = Pool(self.pool_size, self.__init_worker)

        # Private db of stored connections
        self._connections = dict()

    def connect(self, address=None):
        """Connects to the node by creating two sockets for publishing and
        subscribing/receiving messages.

        It returns and the same time stores in the local connection database
        created xMsgConnection object.

        Args:
            address (ProxyAddress): xmsg proxy address object

        Returns:
            xMsgConnection: xmsg connection object
        """
        p_address = address or ProxyAddress()
        return self.__create_connection(self.context, p_address)

    def get_new_connection(self, address):
        """Returns a new xMsgConnection object to the xMsg proxy, using
        new zmq context

        Args:
            address (xMsgAddress): xMsg address object

        Returns:
            connection (xMsgConnection): xMsg connection object
        """
        context = zmq.Context.instance()
        return self.__create_connection(context, address)

    def __create_connection(self, context, p_address):
        connection = xMsgConnection(p_address, xMsgConnectionSetup(),
                                    context.socket(zmq.PUB),
                                    context.socket(zmq.SUB))
        connection.connect()
        return connection

    def destroy(self, linger=-1):
        """ Destroys the created context and terminates the thread pool.

        Args:
            linger (int): milliseconds that the thread will try to send
                messages after the socket has been closed.Default value
                is -1, which in ZMQ means to linger forever.
        """
        self.context.destroy(linger)
        self.__terminate_threadpool()

    def register_as_publisher(self, topic,
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

    def register_as_subscriber(self, topic,
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

    def remove_as_publisher(self, topic):
        """Removes publisher registration both from the local and then from the
        global registration databases

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
        """
        r_data = self._registration_builder(topic, None, True)

        self.driver.remove_registration_local(self.myname, r_data, True)

    def remove_as_subscriber(self, topic):
        """Removes subscriber registration both from the local and then from the
        global registration database

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
        """
        r_data = self._registration_builder(topic, None, False)

        self.driver.remove_registration_local(self.myname, r_data, False)

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

        # Check connection
        if not connection.pub:
            raise NullConnection("xMsg: Null connection object")
        # Check msg
        if not transient_message:
            raise NullMessage("xMsg: Null message object")

        connection.send(transient_message)

    def sync_publish(self, connection, transient_message, timeout):
        # set the return address as replyTo in the xMsgMessage
        return_address = "return: %d" % randint(0, 100)
        return_topic = xMsgTopic.wrap(return_address)
        transient_message.get_metadata().replyTo = return_address

        # subscribe to the return_address
        cb = SyncSendCallBack()
        sh = self.subscribe(return_topic, connection, cb)
        cb.set_handler(sh)
        xMsgUtil.sleep(0.01)
        self.publish(connection, transient_message)
        # wait for the response
        t = 0

        while not cb.received_message:
            xMsgUtil.sleep(0.001)
            if t >= timeout * 1000:
                self.unsubscribe(sh)
                raise Exception("Error: time_out reached - %d" % t)

            else:
                t += 1

        self.unsubscribe(sh)
        cb.received_message.get_metadata().replyTo = str(xMsgConstants.UNDEFINED)

        return cb.received_message

    def subscribe(self, topic, connection, callback):
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
        to the user implemented callback method. Sync and async messaging can
        be obtained by reading the replyTo field at the message metadata

        Args:
            connection (xMsgConnection):  connection object
            topic (xMsgTopic): subscription topic
            callback: user supplied callback function

        Returns:
            xMsgSubscription: xMsg Subscription object, it allows thread handling
        """
        subscription_handler = xMsgSubscription(str(topic), connection)

        def handle(msg):
            self._call_user_callback(connection, callback, msg)

        subscription_handler.set_handle(handle)
        subscription_handler.start()

        return subscription_handler

    def _call_user_callback(self, connection, callback, callback_message):
        requester = callback_message.get_metadata().replyTo
        if requester != str(xMsgConstants.UNDEFINED):
            # Sync request
            try:
                message = callback.callback(callback_message)
                message.set_topic(xMsgTopic.wrap(requester))
                message.get_metadata().replyTo = str(xMsgConstants.UNDEFINED)

                self.publish(connection, message)

            except Exception as e:
                # TODO: proper exception
                raise Exception(e)

        else:
            # now i add the callback execution into the thread pool
            callback.callback(callback_message)

    def unsubscribe(self, subscription):
        subscription.stop()

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


class SyncSendCallBack(xMsgCallBack):
    handler = None
    received_message = None

    def get_message(self):
        return self.received_message

    def set_handler(self, handler):
        self.handler = handler

    def callback(self, msg):
        self.received_message = msg
        if self.handler is not None:
            self.handler.stop()

        return self.received_message
