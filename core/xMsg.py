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
from multiprocessing import Pool
import threading
import signal
import zmq

from core.xMsgExceptions import NullConnection, NullMessage
from core.xMsgConstants import xMsgConstants
from core.xMsgMessage import xMsgMessage
from core.xMsgUtil import xMsgUtil
from data import xMsgRegistration_pb2, xMsgData_pb2, xMsgMeta_pb2
from net.xMsgConnection import xMsgConnection
from xsys.regdis.xMsgRegDriver import xMsgRegDriver
from core.xMsgExceptions import MessageException



__author__ = 'gurjyan'


class xMsg:
    """
    xMsg base class that provides methods for
    organizing pub/sub communications. This class
    provides a local database of xMsgCommunication
    for publishing and/or subscribing messages without
    requesting registration information from the local
    (running within xMsgNode) and/or global (running
    within xMsgFE) registrar services.
    This class also provides a thread pool for servicing
    received messages (as a result of a subscription) in
    separate threads.
    """

    # zmq context object
    driver = str(xMsgConstants.UNDEFINED)

    # Private db of stored connections
    _connections = dict()

    # Fixed size thread pool
    threadPool = str(xMsgConstants.UNDEFINED)
    pool_size = str(xMsgConstants.UNDEFINED)

    def __init__(self, name, feHost, pool_size=2):
        """
        Constructor, requires the name of the FrontEnd host that is used
        to create to the registrar service running within the xMsgFE.
        Creates the zmq context object and thread pool for servicing
        received messages in a separate threads.
        :param feHost: host name of FE
        :param pool_size: thread pool size
        """
        # Name of xMsg Actor
        self.myname = name

        # Initialize registration driver
        self.driver = xMsgRegDriver(feHost)
        self.localhost_ip = xMsgUtil.host_to_ip("localhost")

        # create fixed size thread pool
        self.pool_size = pool_size
        self.threadPool = Pool(self.pool_size, self.init_worker)

    def connect(self, address):
        """
        Connects to the xMsgNode by creating two sockets for publishing and
        subscribing/receiving messages. It returns and the same time stores
        in the local connection database created
        xMsgConnection object.

        :param address: xMsgAddress object
        :return: xMsgConnection object
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
            feCon = xMsgConnection()
            feCon.set_address(address)
            soc_p = self.driver.zmq_socket(self.driver.context,
                                           zmq.PUB,
                                           address.get_host(),
                                           address.get_port(),
                                           str(xMsgConstants.CONNECT))
            feCon.set_pub_sock(soc_p)

            soc_s = self.driver.zmq_socket(self.driver.context,
                                           zmq.SUB,
                                           address.get_host(),
                                           address.get_port() + 1,
                                           str(xMsgConstants.CONNECT))
            feCon.set_sub_sock(soc_s)

            self._connections[address.get_key()] = feCon
            return feCon

    def get_new_connection(self, address):
        """
        Returns a new xMsgConnection object to the xMsg proxy,
        using new zmq context
        :param address: xMsgAddress object
        :return: xMsgConnection object
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

    def register_publisher(self, topic, description=str(xMsgConstants.UNDEFINED)):
        """
        If you are periodically publishing data, use this method to
        register yourself as a publisher with the local registrar.
        This is necessary for future subscribers to discover and
        listen to your messages.

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        """

        r_data = self._registration_builder(topic, description, True)

        self.driver.register_local(self.myname, r_data, True)

    def register_subscriber(self, topic, description=str(xMsgConstants.UNDEFINED)):
        """
        If you are a subscriber and want to listen messages on a specific
        topic from a future publishers, you should register yourself as
        a subscriber with the local registrar.
        Future publishers might express an interest to publish data to a
        a required topic of interest or might publish data only if there
        are active listeners/subscribers to their published topic.

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        """
        r_data = self._registration_builder(topic, description, False)

        self.driver.register_local(self.myname, r_data, False)

    def remove_publisher_registration(self, topic):
        """
        Removes publisher registration both from the local and then from the
        global registration databases

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        """
        r_data = self._registration_builder(topic, None, True)

        self.driver.remove_registration_local(self.myname, r_data, True)
        self.driver.remove_registration_fe(self.myname, r_data, True)

    def remove_subscriber_registration(self, topic):

        """
        Removes subscriber registration both from the local and then from the
        global registration databases

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        """
        r_data = self._registration_builder(topic, None, False)

        self.driver.remove_registration_local(self.myname, r_data, False)
        self.driver.remove_registration_fe(self.myname, r_data, False)

    def find_local_publisher(self, topic, description=str(xMsgConstants.UNDEFINED)):
        """
        Finds all local publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :return: List of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, True)

        return self.driver.find_local(self.myname, r_data, True)

    def find_local_subscriber(self, topic, description=str(xMsgConstants.UNDEFINED)):
        """
        Finds all local subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :return: List of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, False)

        return self.driver.find_local(self.myname, r_data, False)

    def find_publisher(self, topic, description=str(xMsgConstants.UNDEFINED)):
        """
        Finds all publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        :return: List of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, True)

        return self.driver.find_global(self.myname, r_data, True)

    def find_subscriber(self, topic, description=str(xMsgConstants.UNDEFINED)):
        """
        Finds all subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        :return: List of xMsgRegistration objects
        """
        r_data = self._registration_builder(topic, description, False)

        return self.find_global(self.myname, r_data, False)

    def publish(self, connection, msg):
        """
        Publishes data to a specified xMsg topic.3 elements are defining
        xMsg topic: domain:subject:tip
        Topic is obtained in xMsgMessage.topic() method.
        If subject is set "*" type will be ignored. Here are examples of
        accepted topic definitions:<br>
            domain:*:*
            domain:subject:*
            domain:subject:type
        This method will perform input data, i.e. xMsgMessage object
        serialization.

        :param connection: xMsgConnection object
        :param x_msg: xMsgMessage transient data object
        """
        con = connection.get_pub_sock()

        # Check connection
        if not con:
            raise NullConnection("xMsg: Null connection object")
        # Check msg
        if not msg:
            raise NullMessage("xMsg: Null message object")

        data_serial = []
        data_serial.append(str(msg.get_topic()))
        data_serial.append("envelope")
        data_serial.append(msg.get_data())

        con.send_multipart(data_serial)

    def subscribe(self, connection, topic, cb, is_sync):
        t1 = threading.Thread(target=self.__sub_module,
                              args=(connection, topic, cb, is_sync))
        t1.setDaemon(True)
        t1.start()

    def __sub_module(self, connection, topic, cb, is_sync):
        """
        Subscribes to a specified xMsg topic. 3 elements are defining
        xMsg topic: domain:subject:tip
        Topic is constructed from these elements separated by ":"
        Domain is required , however subject and topic can be set to "*".
        If subject is set "*" type will be ignored. Here are examples of
        accepted topic definitions:<br>
            domain:*:*
            domain:subject:*
            domain:subject:tip
        Supplied user callback object must implement xMsgCallBack interface.
        This method will de-serialize received xMsgData object and pass it
        to the user implemented callback method of the interface.
        In the case isSync input parameter is set to be false the method will
        utilize private thread pool to run user callback method in a separate
        thread.

        :param connection: xMsgConnection object
        :param cb: user supplied callback function
        :param isSync: if set to true method will block until user callback
                       method is returned. In case you need to run in a
                       multi-threaded mode,
                       i.e. running parallel user call backs,
                       set is_sync = False
        """

        # get subscribers socket connection
        con = connection.get_sub_sock()

        # subscribe to the topic
        con.setsockopt(zmq.SUBSCRIBE, str(topic))

        # wait for messages published to a required topic
        while True:
            try:
                response = con.recv_multipart()

                if len(response) == 3:

                    # de-serialize response
                    serialized_data = response[2]
                    result = xMsgMessage.create_with_serialized_data(topic,
                                                                     serialized_data)

                    # user callback
                    if is_sync:
                        cb(result)

                    else:
                        # using thread pool
                        # using a new created thread
                        l = [result]
                        t = threading.Thread(target=cb, args=l)
                        t.daemon = True
                        t.start()

            except KeyboardInterrupt:
                return

    def _registration_builder(self, topic, description, publisher=True):
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
        """
        Returns internal thread pool size
        :return size of the thread pool
        """
        return self.pool_size

    def init_worker(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def terminate_threadpool(self):
        self.driver.get_context().destroy()
        self.threadPool.terminate()
        self.threadPool.join()
