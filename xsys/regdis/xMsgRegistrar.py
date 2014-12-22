import threading

import zmq
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from data import xMsgRegistrationData_pb2

from xsys.regdis.xMsgFeRegT import xMsgFeRegT


__author__ = 'gurjyan'

class xMsgRegistrar(threading.Thread):
    """
     The main registrar service, that always runs in a
    separate thread. Contains two separate databases
    to store publishers and subscribers registration data.
    The key for the data base is xMsg topic, constructed as:
    domain:subject:type
    Creates REP socket server on a default port
    Following request will be serviced:
     <ul>
           <li>Register publisher</li>
           <li>Register subscriber</li>
           <li>Find publisher</li>
           <li>Find subscriber</li>
     </ul>

    """

    # zmq context.
    # Note. this class does not own the context.
    context = xMsgConstants.UNDEFINED

    # Database to store publishers
    publishers_db = dict()

    # Database to store subscribers
    subscribers_db = dict()

    # Registrar accepted requests from any host (*)
    host = xMsgConstants.ANY_HOST

    # Default port of the registrar
    port = xMsgConstants.REGISTRAR_PORT

    # Used as a prefix to the name of this registrar.
    # The name of the registrar is used to set the sender field
    # when it creates a request message to be sent to the requester.
    localhost_ip = xMsgUtil.host_to_ip("localhost")

    def __init__(self, context, feHost=None):
        """
        Constructor used by xMSgNode objects.
        xMsgNode needs periodically report/update xMsgFe registration
        database with data stored in its local databases. This process
        makes sure we have proper duplication of the registration data
        for clients seeking global discovery of publishers/subscribers.
        It is true that discovery can be done using xMsgNode registrar
        service only, however by introducing xMsgFE, xMsgNodes can come
        and go, thus making xMsg message-space elastic.

        :param context: zmq context
        :param feHost: Front-End host
        """
        super(xMsgRegistrar, self).__init__()
        self.context = context
        if feHost is not None:
            xMsgFeRegT(feHost, self.publishers_db, self.subscribers_db).start()

    def run(self):

        #  Create registrar REP socket
        request = self.context.socket(zmq.REP)
        request.bind("tcp://%s:%s" % (str(self.host), str(self.port)))

        while True:
            try:
                res = request.recv_multipart()
                r_topic = res[0]
                r_sender = res[1]
                r_data = res[2]

                print " Received a request from " + r_sender + " to " + r_topic

                # de-serialize r_data
                ds_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
                ds_data.ParseFromString(r_data)

                s_host = xMsgConstants.UNDEFINED
                key = xMsgConstants.UNDEFINED

                if r_topic == xMsgConstants.REMOVE_ALL_REGISTRATION:
                    s_host = r_data
                else:
                    key = ds_data.domain
                    if ds_data.subject != xMsgConstants.UNDEFINED:
                        key = key + ":" + ds_data.subject
                    if ds_data.xtype != xMsgConstants.UNDEFINED:
                        key = key + ":" + ds_data.xtype

                if r_topic == xMsgConstants.REGISTER_PUBLISHER:
                    self.publishers_db[key] = ds_data

                    # send a reply message
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            xMsgConstants.SUCCESS])

                elif r_topic == xMsgConstants.REGISTER_SUBSCRIBER:

                    self.subscribers_db[key] = ds_data
                    # send a reply message
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            xMsgConstants.SUCCESS])

                elif r_topic == xMsgConstants.REMOVE_PUBLISHER:
                    del self.publishers_db[key]
                    # send a reply message
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            xMsgConstants.SUCCESS])

                elif r_topic == xMsgConstants.REMOVE_SUBSCRIBER:
                    del self.subscribers_db[key]
                    # send a reply message
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            xMsgConstants.SUCCESS])

                elif r_topic == xMsgConstants.REMOVE_ALL_REGISTRATION:
                    # Remove publishers registration data from a specified host
                    self._cleanDbByHost(s_host, self.publishers_db)

                    # Remove subscribers registration data from a specified host
                    self._cleanDbByHost(s_host, self.subscribers_db);
                    # send a reply message
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            xMsgConstants.SUCCESS])

                elif r_topic == xMsgConstants.FIND_PUBLISHER:

                    res = self._getRegistration(ds_data.domain, ds_data.subject, ds_data.xtype, True)
                    d = []
                    for rd in res:
                        # Serialize and add to the reply message
                        s_rd = rd.SerializeToString()
                        d.append(s_rd)

                    s_dt = xMsgUtil.list_to_string(d)
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            s_dt])

                elif r_topic == xMsgConstants.FIND_SUBSCRIBER:

                    res = self._getRegistration(ds_data.domain, ds_data.subject, ds_data.xtype, False)
                    d = []
                    for rd in res:
                        # Serialize and add to the reply message
                        s_rd = rd.SerializeToString()
                        d.append(s_rd)

                    s_dt = xMsgUtil.list_to_string(d)
                    request.send_multipart([r_topic,
                                            xMsgUtil.get_local_ip() + ":" + xMsgConstants.REGISTRAR,
                                            s_dt])
                else:
                    print " Warning: unknown registration request type..."

            except KeyboardInterrupt:
                    return

    def _getRegistration(self, domain, subject, tip, isPublisher):
        """
        This method finds registration data in the database based on
        a match of the xMsg registration database-key components.
        We assume that domain element of the key  is always defined,
        but subject and types can be set to be undefined. So, what we
        do here is to create a list containing only defined components
        of the input key, and retrieve registration objects of those
        database keys containing defined elements of the input key.

        :param domain: xMsg domain
        :param subject: xMsg subject
        :param tip: xMsg type (note: type is a python keyword)
        :param isPublisher: defines what database to look for
        :return: set of xMsgRegistrationData object
        """

        # create a list containing defined input key elements
        st = [domain]
        if subject != xMsgConstants.UNDEFINED:
            st.append(subject)
        if tip != xMsgConstants.UNDEFINED:
            st.append(tip)

        result = list()

        if isPublisher:
            for k in self.publishers_db:
                for s in st:
                    if s in k:
                        x = self.publishers_db[k]
                        if x not in result:
                            result.append(x)
        else:
            for k in self.subscribers_db:
                for s in st:
                    if s in k:
                        x = self.subscribers_db[k]
                        if x not in result:
                            result.append(x)
        return result

    def _cleanDbByHost(self, host, db):
        """
        Method that removes all values of the registration database that
        have a specified host set, i.e.  removes registration information
        of all xMsg actors that are running on a specified host.

        :param host: host name of the xMsgNode
        :param db: reference to the registration database
        """

        # First create a list of keys that match the criteria, to
        # be used for removing the registration data for those keys
        rk = []

        for k in db:
            if db[k].host == host:
                rk.append(k)
        #Remove all identified keys
        for k in rk:
            db.remove(k)

