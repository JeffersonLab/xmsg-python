# coding=utf-8
from contextlib import contextmanager
from random import randint

import zmq

from xmsg.core.ConnectionManager import ConnectionManager
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgExceptions import NullConnection, NullMessage
from xmsg.core.xMsgSubscription import xMsgSubscription
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data.xMsgRegistration_pb2 import xMsgRegistration
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress
from xmsg.net.xMsgConnection import xMsgConnection


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

    def __init__(self, name, proxy_address=None,
                 registrar_address=None, **kwargs):
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

        # Set of subscriptions
        self.my_subscriptions = []

        context = kwargs.pop("context", False)
        self.context = context or zmq.Context.instance()

        if proxy_address:
            if isinstance(proxy_address, basestring):
                self.default_proxy_address = ProxyAddress(proxy_address)
            elif isinstance(proxy_address, ProxyAddress):
                self.default_proxy_address = proxy_address
        else:
            self.default_proxy_address = ProxyAddress()

        if registrar_address:
            if isinstance(registrar_address, basestring):
                self.default_registrar_address = RegAddress(registrar_address)
            elif isinstance(registrar_address, RegAddress):
                self.default_registrar_address = registrar_address
        else:
            self.default_registrar_address = RegAddress()

        # Initialize registration driver
        self.connection_manager = ConnectionManager(self.context)

    def __repr__(self):
        return str("<xMsg : %s>" % self.myname)

    def get_connection(self, address):
        """Connects to the node by creating two sockets for publishing and
        subscribing/receiving messages.

        It returns and the same time stores in the local connection database
        created xMsgConnection object.

        Args:
            address (ProxyAddress): xmsg proxy address

        Returns:
            xMsgConnection: xMsg connection handler
        """
        return xMsgConnection(self.connection_manager,
                              self.connection_manager.get_proxy_connection(address))

    def release(self, connection):
        """ Returns the given connection into the pool of available connections

        Args:
            connection (xMsgProxyDriver): connection object
        """
        self.connection_manager.release_proxy_connection(connection)

    def destroy(self, linger=-1):
        """ Destroys the created context and terminates the thread pool.

        Args:
            linger (int): milliseconds that the thread will try to send
                messages after the socket has been closed.Default value
                is -1, which in ZMQ means to linger forever.
        """
        self.context.destroy(linger)

    def register_as_publisher(self, address, topic,
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
        self._register(address, topic, description, True)

    def register_as_subscriber(self, address, topic,
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
        self._register(address, topic, description, False)

    def remove_as_publisher(self, address, topic):
        """Removes publisher registration both from the local and then from the
        global registration databases

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
        """
        self._remove_registration(address, topic, "None", True)

    def remove_as_subscriber(self, address, topic):
        """Removes subscriber registration both from the local and then from the
        global registration database

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)
        """

        self._remove_registration(address, topic, "None", False)

    def find_publisher(self, address, topic):
        """
        Finds all publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)

        Returns:
            list: list of xMsgRegistration objects
        """
        return self._find_registration(address, topic, True)

    def find_subscriber(self, topic, address):
        """
        Finds all subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        Args:
            topic (xMsgTopic): the name of the requester/sender. Required
                according to the xMsg zmq message structure definition
                (topic, sender, data)

        Returns:
            list: list of xMsgRegistration objects
        """
        return self._find_registration(address, topic, False)

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
            connection (xMsgConnection): proxy communication driver
            transient_message (xMsgMessage): transient data object

        Raises:
            NullConnection: if there is no connection object
            NullMessage: if there is no message object
        """

        # Check connection
        if not connection:
            raise NullConnection("xMsg: Null connection object")
        # Check msg
        if not transient_message:
            raise NullMessage("xMsg: Null message object")

        assert isinstance(connection, xMsgConnection)

        with self._closing(connection):
            connection.publish(transient_message)

    def sync_publish(self, connection, transient_message, timeout):
        """Publishes a message through the specified proxy connection and
        blocks waiting for a response.

        The subscriber must publish the response to the topic given by the
        reply_to metadata field, through the same proxy.

        This method will throw if a response is not received before the timeout
        expires.
        """

        # set the return address as replyTo in the xMsgMessage
        return_address = "return: %d" % randint(0, 100)
        return_topic = xMsgTopic.wrap(return_address)
        transient_message.metadata.replyTo = return_address

        # subscribe to the return_address
        sync_callback = _SyncSendCallBack()
        subscription_handler = self.subscribe(connection.get_address(),
                                              return_topic,
                                              sync_callback)
        sync_callback.set_handler(subscription_handler)

        self.publish(connection, transient_message)
        # wait for the response
        time_counter = 0

        while not sync_callback.received_message:
            xMsgUtil.sleep(0.001)
            if time_counter >= timeout * 1000:
                self.unsubscribe(subscription_handler)
                raise Exception("Error: time_out reached - %d" % time_counter)

            else:
                time_counter += 1

        self.unsubscribe(subscription_handler)
        sync_callback.received_message.metadata.replyTo = str(xMsgConstants.UNDEFINED)

        return sync_callback.received_message

    def subscribe(self, address, topic, callback):
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
            address (ProxyAddress):  connection object
            topic (xMsgTopic): subscription topic
            callback (xMsgCallBack): user supplied callback function

        Returns:
            xMsgSubscription: xMsg Subscription object, it allows thread handling
        """
        connection = self.get_connection(address)
        driver = self.connection_manager.get_proxy_connection(address)
        subscription_handler = xMsgSubscription(str(topic), driver)

        def _callback(msg):
            self._call_user_callback(connection, callback, msg)

        subscription_handler.set_callback_func(_callback)
        self.my_subscriptions.append(subscription_handler)
        subscription_handler.start()
        return subscription_handler

    def _call_user_callback(self, connection, callback, t_message):
        if t_message.metadata.replyTo:
            # Sync request
            try:
                r_message = callback.callback(t_message)
                r_message.topic = xMsgTopic.wrap(t_message.metadata.replyTo)
                r_message.metadata.replyTo = str(xMsgConstants.UNDEFINED)

                self.publish(connection, r_message)

            except zmq.error.ZMQError as zmq_error:
                raise Exception(zmq_error)

        else:
            callback.callback(t_message)

    def unsubscribe(self, subscription):
        """Stops the given subscription

        Args:
            subscription (xMsgSubscription): given subscription to unsubscribe
        """
        subscription.stop()

    def _register(self, address, topic, description, publisher):
        registration_driver = self.connection_manager.get_registrar_connection(address)
        reg_data = self._registration_builder(topic, description, publisher)
        registration_driver.add(reg_data, publisher)

    def _remove_registration(self, address, topic, description, publisher):
        registration_driver = self.connection_manager.get_registrar_connection(address)
        reg_data = self._registration_builder(topic, description, publisher)
        registration_driver.remove(reg_data, publisher)

    def _find_registration(self, address, topic, publisher):
        registration_driver = self.connection_manager.get_registrar_connection(address)
        reg_data = self._registration_builder(topic, str(xMsgConstants.UNDEFINED),
                                              publisher)
        return registration_driver.find(reg_data, publisher)

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
        r_data = xMsgRegistration()
        r_data.name = self.myname
        if description:
            r_data.description = description
        r_data.host = topic.domain()
        r_data.port = int(xMsgConstants.DEFAULT_PORT)
        r_data.domain = topic.domain()
        r_data.subject = topic.subject()
        r_data.type = topic.type()

        if publisher:
            r_data.ownerType = xMsgRegistration.PUBLISHER
        else:
            r_data.ownerType = xMsgRegistration.SUBSCRIBER

        return r_data

    @contextmanager
    def _closing(self, conn):
        try:
            yield conn

        except Exception as e:
            print e.message
            raise e
        finally:
            conn.close()


class _SyncSendCallBack(xMsgCallBack):

    def __init__(self):
        self.received_message = None
        self.handler = None

    def set_handler(self, handler):
        """Sets the subscription handler for the sync callback
        Args
            handler (xMsgSubscription): sync subscription handler
        """
        self.handler = handler

    def callback(self, msg):
        self.received_message = msg
        if self.handler:
            self.handler.stop()
        return msg
