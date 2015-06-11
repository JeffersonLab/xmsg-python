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

from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from data import xMsgRegistration_pb2, xMsgData_pb2
from net.xMsgConnection import xMsgConnection
from xsys.regdis.xMsgRegDiscDriver import xMsgRegDiscDriver
from core.xMsgExceptions import UndefinedTopicDomain, NullConnection,\
    NullMessage


__author__ = 'gurjyan'


class xMsg(xMsgRegDiscDriver):
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
    # _context = xMsgConstants.UNDEFINED

    # Private db of stored connections
    _connections = dict()

    # Fixed size thread pool
    threadPool = str(xMsgConstants.UNDEFINED)
    pool_size = str(xMsgConstants.UNDEFINED)

    def __init__(self, feHost, pool_size=2):
        """
        Constructor, requires the name of the FrontEnd host that is used
        to create to the registrar service running within the xMsgFE.
        Creates the zmq context object and thread pool for servicing
        received messages in a separate threads.
        :param feHost: host name of FE
        :param pool_size: thread pool size
        """
        xMsgRegDiscDriver.__init__(self, feHost)
        # self._context = self.getContext()

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
            soc_p = self.zmq_socket(self.context,
                                    zmq.PUB,
                                    address.get_host(),
                                    address.get_port(),
                                    str(xMsgConstants.CONNECT))
            feCon.set_pub_sock(soc_p)

            soc_s = self.zmq_socket(self.context,
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
        soc_p = self.zmq_socket(new_context,
                                zmq.PUB,
                                address.get_host(),
                                address.get_port(),
                                str(xMsgConstants.CONNECT))
        feCon.set_pub_sock(soc_p)

        soc_s = self.zmq_socket(new_context,
                                zmq.SUB,
                                address.get_host(),
                                address.get_port() + 1,
                                str(xMsgConstants.CONNECT))
        feCon.set_sub_sock(soc_s)
        return feCon

    def register_publisher(self, name,
                           domain,
                           subject,
                           xtype,
                           description=str(xMsgConstants.UNDEFINED),
                           host="localhost",
                           port=int(xMsgConstants.DEFAULT_PORT)):
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

        r_data = self._registration_builder(name, description,
                                            xMsgUtil.host_to_ip(host),
                                            port, domain, subject,
                                            xtype, True)

        self.register_local(name, r_data, True)

    def register_subscriber(self, name,
                            domain,
                            subject,
                            xtype,
                            description=str(xMsgConstants.UNDEFINED),
                            host="localhost",
                            port=int(xMsgConstants.DEFAULT_PORT)):
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
        r_data = self._registration_builder(name, description,
                                            xMsgUtil.host_to_ip(host),
                                            port, domain, subject,
                                            xtype, False)

        self.register_local(name, r_data, False)

    def remove_publisher_registration(self, name,
                                      domain,
                                      subject,
                                      xtype,
                                      host="localhost",
                                      port=int(xMsgConstants.DEFAULT_PORT)):
        """
        Removes publisher registration both from the local and then from the
        global registration databases

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        """
        r_data = self._registration_builder(name, None,
                                            xMsgUtil.host_to_ip(host),
                                            port, domain, subject,
                                            xtype, True)

        self.remove_registration_local(name, r_data, True)
        self.remove_registration_fe(name, r_data, True)

    def remove_subscriber_registration(self, name,
                                       domain,
                                       subject,
                                       xtype,
                                       host="localhost",
                                       port=int(xMsgConstants.DEFAULT_PORT)):

        """
        Removes subscriber registration both from the local and then from the
        global registration databases

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :param r_data: xMsgRegistration object
        """
        r_data = self._registration_builder(name, None,
                                            xMsgUtil.host_to_ip(host),
                                            port, domain, subject,
                                            xtype, False)

        self.remove_registration_local(name, r_data, False)
        self.remove_registration_fe(name, r_data, False)

    def find_local_publisher(self, name,
                             domain,
                             subject,
                             xtype,
                             description=str(xMsgConstants.UNDEFINED),
                             port=int(xMsgConstants.DEFAULT_PORT)):
        """
        Finds all local publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :return: List of xMsgRegistration objects
        """
        r_data = self._registration_builder(name, description,
                                            xMsgUtil.host_to_ip("localhost"),
                                            port, domain, subject,
                                            xtype, True)

        return self.find_local(name, r_data, True)

    def find_local_subscriber(self, name,
                              domain,
                              subject,
                              xtype,
                              description=str(xMsgConstants.UNDEFINED),
                              port=int(xMsgConstants.DEFAULT_PORT)):
        """
        Finds all local subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistration
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition.
                     (topic, sender, data)
        :return: List of xMsgRegistration objects
        """
        r_data = self._registration_builder(name, description,
                                            xMsgUtil.host_to_ip("localhost"),
                                            port, domain, subject,
                                            xtype, False)

        return self.find_local(name, r_data, False)

    def find_publisher(self, name,
                       domain,
                       subject,
                       xtype,
                       host,
                       description=str(xMsgConstants.UNDEFINED),
                       port=int(xMsgConstants.DEFAULT_PORT)):
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
        r_data = self._registration_builder(name, description,
                                            xMsgUtil.host_to_ip(host),
                                            port, domain, subject,
                                            xtype, True)

        return self.find_global(name, r_data, True)

    def find_subscriber(self, name,
                        domain,
                        subject,
                        xtype,
                        host,
                        description=str(xMsgConstants.UNDEFINED),
                        port=int(xMsgConstants.DEFAULT_PORT)):
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
        r_data = self._registration_builder(name, description,
                                            xMsgUtil.host_to_ip(host),
                                            port, domain, subject,
                                            xtype, False)

        return self.find_global(name, r_data, False)

    def publish(self, connection, x_msg):
        """
        Publishes data to a specified xMsg topic.3 elements are defining
        xMsg topic: domain:subject:tip
        Topic is obtained in xMsgMessage.get_topic() method.
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
        if not con:
            raise NullConnection("xMsg: Null connection object")
        if not x_msg:
            raise NullMessage("xMsg: Null message object")

        con.send_multipart([x_msg.get_topic(),
                            x_msg.get_metadata_bytes(),
                            x_msg.get_data_bytes()])

    def subscribe(self, connection,
                  domain,
                  subject,
                  tip,
                  cb,
                  isSync):

        t1 = threading.Thread(target=self.__sub_module, args=(connection,
                                                              domain,
                                                              subject,
                                                              tip,
                                                              cb,
                                                              isSync))
        t1.setDaemon(True)
        t1.start()

    def __sub_module(self, connection,
                     domain,
                     subject,
                     tip,
                     cb,
                     isSync):
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
        :param domain: domain of the subscription
        :param subject: subject of the subscription
        :param tip: type of the subscription (type is a python keyword,
                    i.e. we use tip)
        :param cb: user supplied callback function
        :param isSync: if set to true method will block until user callback
                       method is returned. In case you need to run in a
                       multi-threaded mode,
                       i.e. running parallel user call backs,
                       set isSync = False
        """

        # get subscribers socket connection
        con = connection.get_sub_sock()

        # build a topic
        if domain == str(xMsgConstants.ANY) or domain is None:
            raise UndefinedTopicDomain("domain is not defined")
        else:
            topic = domain
            if subject is not None and subject != str(xMsgConstants.ANY):
                topic = topic + ":" + subject
                if tip is not None and tip != str(xMsgConstants.ANY):

                    # Note that type can also have *
                    # for e.g. topic for error/warning/info broadcasting
                    # the type is the name of the service broadcasting the
                    # message.
                    # Service name can contain * indicating any
                    # domain/container/engine
                    # here we handle that type of cases.
                    tl = tip.split(":")
                    for ts in tl:
                        if "*" is not ts:
                            topic = topic + ":" + ts
                        else:
                            break

        # subscribe to the topic
        con.setsockopt(zmq.SUBSCRIBE, topic)
        # con.subscribe(topic)

        # wait for messages published to a required topic
        while True:
            try:
                res = con.recv_multipart()
                if len(res) == 3:
                    # r_topic = res[0]
                    # r_sender = res[1]
                    r_data = res[2]

                    # de-serialize r_data
                    ds_data = xMsgData_pb2.xMsgData()
                    ds_data.ParseFromString(r_data)
                    result = ds_data

                    # usr callback
                    if isSync:
                        cb(result)
                    else:
                        # using thread pool
                        # self.threadPool.apply_async(cb, result)
                        # using a new created thread
                        l = [result]
                        t = threading.Thread(target=cb, args=l)
                        t.daemon = True
                        t.start()

            except KeyboardInterrupt:
                return

    def _registration_builder(self, name, description, host, port,
                              domain, subject, xtype, publisher=True):
        r_data = xMsgRegistration_pb2.xMsgRegistration()
        r_data.name = name
        if description:
            r_data.description = description
        r_data.host = xMsgUtil.host_to_ip(host)
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.type = xtype

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
        self.context.destroy()
        self.threadPool.terminate()
        self.threadPool.join()
