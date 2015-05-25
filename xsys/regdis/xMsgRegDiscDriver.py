import zmq

from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from data import xMsgRegistrationData_pb2


__author__ = 'gurjyan'


class xMsgRegDiscDriver:

    # Front-end registrar server (req/rep) connection socket
    _feConnection = str(xMsgConstants.UNDEFINED)

    # Local registrar server (req/rep) connection socket
    _lnConnection = str(xMsgConstants.UNDEFINED)

    # zmq context
    context = str(xMsgConstants.UNDEFINED)

    def __init__(self, feHost=None):
        self.context = zmq.Context()

        if feHost is None:

            self._lnConnection = self.zmqSocket(self.context, zmq.REQ,
                                                xMsgUtil.host_to_ip("localhost"),
                                                int(xMsgConstants.REGISTRAR_PORT),
                                                str(xMsgConstants.CONNECT))
            self._feConnection = self._lnConnection
        else:
            self._feConnection = self.zmqSocket(self.context, zmq.REQ,
                                                xMsgUtil.host_to_ip(feHost),
                                                int(xMsgConstants.REGISTRAR_PORT),
                                                str(xMsgConstants.CONNECT))

            self._lnConnection = self.zmqSocket(self.context, zmq.REQ,
                                                xMsgUtil.host_to_ip("localhost"),
                                                int(xMsgConstants.REGISTRAR_PORT),
                                                str(xMsgConstants.CONNECT))

    def getContext(self):
        """
        Returns the main zmq socket context
        :return zmq context
        """
        return self.context

    def _register(self, connectionSocket, name, data, isPublisher):
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
            # Topic of the message is a string = "registerPublisher" or "registerSubscriber"
            if isPublisher:
                topic = str(xMsgConstants.REGISTER_PUBLISHER)
            else:
                topic = str(xMsgConstants.REGISTER_SUBSCRIBER)

            # Sender
            sender = name

            # Sending...
            connectionSocket.send_multipart([str(topic), str(sender), str(dt)])

            #  Poll socket for a reply, with timeout, make sure server is up and running
            poller = zmq.Poller()
            poller.register(connectionSocket, zmq.POLLIN)
            if poller.poll(int(xMsgConstants.REGISTER_REQUEST_TIMEOUT) * 1000):  # timeout in milliseconds
                msg = connectionSocket.recv_multipart()
                r_topic = msg[0]
                r_sender = msg[1]
                r_data = msg[2]
                # data sent back from the registration server should a string = "success"
                if r_data != str(xMsgConstants.SUCCESS):
                    raise Exception("ERROR: Registration failed")
            else:
                raise Exception("Timeout processing registration request")

    def _remove_registration(self, connectionSocket, name, data, isPublisher):
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
            # Topic of the message is a string = "registerPublisher"
            # or "registerSubscriber"
            if isPublisher:
                topic = str(xMsgConstants.REMOVE_PUBLISHER)
            else:
                topic = str(xMsgConstants.REMOVE_SUBSCRIBER)

            # Sender
            sender = name

            # Sending...
            connectionSocket.send_multipart([str(topic), str(sender), str(dt)])

            # Poll socket for a reply, with timeout, make sure server is up
            # and running
            poller = zmq.Poller()
            poller.register(connectionSocket, zmq.POLLIN)
            if poller.poll(int(xMsgConstants.REGISTER_REQUEST_TIMEOUT) * 1000):
                msg = connectionSocket.recv_multipart()
                r_topic = msg[0]
                r_sender = msg[1]
                r_data = msg[2]

                if r_data != str(xMsgConstants.SUCCESS):
                    raise Exception("failed")
            else:
                raise Exception("Timeout processing registration request")

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

        # Sender
        sender = name

        # data = host of the xMsgNode
        dt = host

        # Sending...
        self._feConnection.send_multipart([str(topic), str(sender), str(dt)])

        poller = zmq.Poller()
        poller.register(self._feConnection, zmq.POLLIN)
        if poller.poll(int(xMsgConstants.REGISTER_REQUEST_TIMEOUT) * 1000):  # timeout in milliseconds
            msg = self._feConnection.recv_multipart()
            r_topic = msg[0]
            r_sender = msg[1]
            r_data = msg[2]

            if r_data != str(xMsgConstants.SUCCESS):
                raise Exception("ERROR: Remove all registration from FrontEnd Failed")
        else:
            raise Exception("Timeout processing registration request")

    def _find(self, connectionSocket, name, data, isPublisher):
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
            dt = data.SerializeToString()

            # Send topic, sender, followed by the data
            # Topic of the message is a string = "findPublisher"
            # or "findSubscriber"
            if isPublisher:
                topic = str(xMsgConstants.FIND_PUBLISHER)
            else:
                topic = str(xMsgConstants.FIND_SUBSCRIBER)

            # Sender
            sender = name

            # Sending...
            connectionSocket.send_multipart([str(topic), str(sender), str(dt)])

            #  Poll socket for a reply, with timeout, make sure server is up and running
            poller = zmq.Poller()
            poller.register(connectionSocket, zmq.POLLIN)
            if poller.poll(int(xMsgConstants.FIND_REQUEST_TIMEOUT) * 1000):  # timeout in milliseconds
                msg = connectionSocket.recv_multipart()
                r_topic = msg[0]
                r_sender = msg[1]
                result = []
                r_data = msg[2:]
                for r_d in r_data:
                    ds_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
                    ds_data.ParseFromString(r_d)
                    result.append(ds_data)
                return result

    def register_fe(self, name, data, isPublisher):
        """
        Registers xMsg actor with the front-end registration and discovery
        server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._register(self._feConnection, name, data, isPublisher)

    def register_local(self, name, data, isPublisher):
        """
        Registers xMsg actor with the local registration and discovery server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._register(self._lnConnection, name, data, isPublisher)

    def removeRegistration_fe(self, name, data, isPublisher):
        """
        Removes xMsg actor from the front-end registration and discovery server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._remove_registration(self._feConnection, name, data, isPublisher)

    def removeRegistration_local(self, name, data, isPublisher):
        """
        Removes xMsg actor from the local registration and discovery server
        :param name: the name of the requester/sender
        :param data: xMsgRegistrationData object
        :param isPublisher: if set to be true then this is a request to
                            register a publisher, otherwise this is a
                            subscriber registration request
        """
        self._remove_registration(self._lnConnection, name, data, isPublisher)

    def findLocal(self, name, data, isPublisher):
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
        return self._find(self._lnConnection, name, data, isPublisher)

    def findGlobal(self, name, data, isPublisher):
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
        return self._find(self._feConnection, name, data, isPublisher)

    def zmqSocket(self, context, socket_type, h, port, boc):
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
