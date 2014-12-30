from multiprocessing import Pool

import zmq

from core.xMsgConstants import xMsgConstants
from data import xMsgRegistrationData_pb2
from data import xMsgData_pb2
from net.xMsgConnection import xMsgConnection
from xsys.regdis.xMsgRegDiscDriver import xMsgRegDiscDriver


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
    threadPool = xMsgConstants.UNDEFINED
    pool_size = xMsgConstants.UNDEFINED

    def __init__(self, feHost, pool_size=16):
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
        self.threadPool = Pool(self.pool_size)

    # pool = Pool(4)              # start 4 worker processes
    # result = pool.apply_async(f, [10])    # evaluate "f(10)" asynchronously
    # print result.get(1)           # prints "100" unless your computer is *very* slow
    # print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"

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
        if address.getKey in self._connections.keys():
            return self._connections.get(address.getKey())
        else:
            # Otherwise create sockets to the
            # requested address, and store the created
            # connection object for the future use.
            # Return the reference to the connection object
            feCon = xMsgConnection()
            feCon.setAddress(address)
            soc_p = self.zmqSocket(self.context,
                                   zmq.PUB,
                                   address.getHost(),
                                   address.getPort(),
                                   xMsgConstants.CONNECT)
            feCon.setPubSock(soc_p)

            soc_s = self.zmqSocket(self.context,
                                   zmq.SUB,
                                   address.getHost(),
                                   address.getPort() + 1,
                                   xMsgConstants.CONNECT)
            feCon.setSubSock(soc_s)

            self._connections[address.getKey()] = feCon
            return feCon

    def registerPublisher(self, name,
                          domain,
                          subject,
                          xtype,
                          host="localhost",
                          port=xMsgConstants.DEFAULT_PORT):
        """
        If you are periodically publishing data, use this method to
        register yourself as a publisher with the local registrar.
        This is necessary for future subscribers to discover and
        listen to your messages.

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        """

        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.PUBLISHER

        self.register_local(name, r_data, True)

    def registerSubscriber(self, name,
                           domain,
                           subject,
                           xtype,
                           host="localhost",
                           port=xMsgConstants.DEFAULT_PORT):
        """
        If you are a subscriber and want to listen messages on a specific
        topic from a future publishers, you should register yourself as
        a subscriber with the local registrar.
        Future publishers might express an interest to publish data to a
        a required topic of interest or might publish data only if there
        are active listeners/subscribers to their published topic.

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        """

        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.SUBSCRIBER

        self.register_local(name, r_data, False)

    def removePublisherRegistration(self, name,
                                    domain,
                                    subject,
                                    xtype,
                                    host="localhost",
                                    port=xMsgConstants.DEFAULT_PORT):
        """
        Removes publisher registration both from the local and then from the
        global registration databases

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        """
        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.PUBLISHER

        self.removeRegistration_local(name, r_data, True)
        self.removeRegistration_fe(name, r_data, True)

    def removeSubscriberRegistration(self, name,
                                     domain,
                                     subject,
                                     xtype,
                                     host="localhost",
                                     port=xMsgConstants.DEFAULT_PORT):

        """
        Removes subscriber registration both from the local and then from the
        global registration databases

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        """
        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.SUBSCRIBER

        self.removeRegistration_local(name, r_data, False)
        self.removeRegistration_fe(name, r_data, False)

    def findLocalPublisher(self, name,
                           domain,
                           subject,
                           xtype,
                           host="localhost",
                           port=xMsgConstants.DEFAULT_PORT):
        """
        Finds all local publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistrationData
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        :return: List of xMsgRegistrationData objects
        """
        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.PUBLISHER

        return self.findLocal(name, r_data, True)

    def findLocalSubscriber(self, name,
                            domain,
                            subject,
                            xtype,
                            host="localhost",
                            port=xMsgConstants.DEFAULT_PORT):
        """
        Finds all local subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistrationData
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        :return: List of xMsgRegistrationData objects
        """
        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.SUBSCRIBER

        return self.findLocal(name, r_data, False)

    def findPublisher(self, name,
                      domain,
                      subject,
                      xtype,
                      host="localhost",
                      port=xMsgConstants.DEFAULT_PORT):
        """
        Finds all publishers, publishing  to a specified topic
        defined within the input registration data object: xMsgRegistrationData
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        :return: List of xMsgRegistrationData objects
        """
        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.PUBLISHER

        return self.findGlobal(name, r_data, True)

    def findSubscriber(self, name,
                       domain,
                       subject,
                       xtype,
                       host="localhost",
                       port=xMsgConstants.DEFAULT_PORT):
        """
        Finds all subscribers, subscribing  to a specified topic
        defined within the input registration data object: xMsgRegistrationData
        Note: xMsg defines a topic as domain:subject:type

        :param name: the name of the requester/sender. Required according to
                     the xMsg zmq message structure definition. (topic, sender, data)
        :param r_data: xMsgRegistrationData object
        :return: List of xMsgRegistrationData objects
        """
        r_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
        r_data.host = host
        r_data.port = port
        r_data.domain = domain
        r_data.subject = subject
        r_data.xtype = xtype
        r_data.ownerType = xMsgRegistrationData_pb2.xMsgRegistrationData.SUBSCRIBER

        return self.findGlobal(name, r_data, False)

    def publish(self, connection, domain, subject, tip, publisherName, data):
        """
        Publishes data to a specified xMsg topic. 3 elements are defining xMsg topic:
        domain:subject:tip
        Topic is constructed from these elements separated by ":"
        Domain is required , however subject and topic can be set to "*".
        If subject is set "*" type will be ignored. Here are examples of
        accepted topic definitions:<br>
            domain:*:*
            domain:subject:*
            domain:subject:tip
        This method will perform input data, i.e. xMsgData object serialization.

        :param connection: xMsgConnection object
        :param domain: domain of the subscription
        :param subject: subject of the subscription
        :param tip: type of the subscription (type is a python keyword, i.e. we use tip)
        :param publisherName: sender/publisher name
        :param data: xMsgData transient data object
        """
        # get publishing socket
        con = connection.getPubSock()

         # build a topic
        if domain is None or domain == "*":
            raise Exception("domain is not defined")
        else:
            topic = domain
            if subject is not None and subject != "*":
                topic = topic + ":" + subject
                if tip is not None and tip != "*":
                    topic = topic + ":" + tip

        # print data.author
        # print data.id
        # print data.dataDescription
        # print data.xtype
        # print len(data.FLSINT32A)

        # data serialization
        s_data = data.SerializeToString()

        # send topic, sender, followed by the data
        con.send_multipart([str(topic), str(publisherName), str(s_data)])

    def subscribe(self, connection, domain, subject, tip, cb, isSync):
        """
        Subscribes to a specified xMsg topic. 3 elements are defining xMsg topic:
        domain:subject:tip
        Topic is constructed from these elements separated by ":"
        Domain is required , however subject and topic can be set to "*".
        If subject is set "*" type will be ignored. Here are examples of
        accepted topic definitions:<br>
            domain:*:*
            domain:subject:*
            domain:subject:tip
        Supplied user callback object must implement xMsgCallBack interface.
        This method will de-serialize received xMsgData object and pass it
        to the user implemented callback method of thee interface.
        In the case isSync input parameter is set to be false the method will
        utilize private thread pool to run user callback method in a separate thread.

        :param connection: xMsgConnection object
        :param domain: domain of the subscription
        :param subject: subject of the subscription
        :param tip: type of the subscription (type is a python keyword, i.e. we use tip)
        :param cb: user supplied callback function
        :param isSync: if set to true method will block until subscription method is
                       received and user callback method is returned
        """

        # get subscribers socket connection
        con = connection.getSubSock()

         # build a topic
        if domain is None or domain == "*":
            raise Exception("domain is not defined")
        else:
            topic = domain
            if subject is not None and subject != "*":
                topic = topic + ":" + subject
                if tip is not None and tip != "*":
                    topic = topic + ":" + tip

        # subscribe to the topic
        con.setsockopt(zmq.SUBSCRIBE, topic)
        # con.subscribe(topic)

        # wait for messages published to a required topic
        while True:
            try:
                # res = connection.recv_multipart()
                res = con.recv_multipart()
                r_topic = res[0]
                r_sender = res[1]
                r_data = res[2]

                # de-serialize r_data
                ds_data = xMsgData_pb2.Data()
                ds_data.ParseFromString(r_data)
                result = ds_data

                # usr callback
                if isSync:
                    cb(result)
                else:
                    self.threadPool.apply_async(cb, result)
            except KeyboardInterrupt:
                    return

    def getPool_size(self):
        """
        Returns internal thread pool size
        :return size of the thread pool
        """
        return self.pool_size