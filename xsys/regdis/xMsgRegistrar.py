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

    # Note. this class does not own the context.
    context = str(xMsgConstants.UNDEFINED)

    # Database to store publishers
    publishers_db = dict()

    # Database to store subscribers
    subscribers_db = dict()

    # Registrar accepted requests from any host (*)
    host = str(xMsgConstants.ANY)

    # Default port of the registrar
    port = int(xMsgConstants.REGISTRAR_PORT)

    # Used as a prefix to the name of this registrar.
    # The name of the registrar is used to set the sender field
    # when it creates a request message to be sent to the requester.
    localhost_ip = xMsgUtil.host_to_ip("localhost")

    stop_request = str(xMsgConstants.UNDEFINED)

    def __init__(self, context, feHost=None):
        """
        Constructor used by xMsgNode objects.
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
        self.stop_request = threading.Event()

        if feHost is not None:
            xMsgFeRegT(feHost, self.publishers_db, self.subscribers_db).start()

    def run(self):

        # Create registrar REP socket
        request = self.context.socket(zmq.REP)
        request.bind("tcp://%s:%s" % (str(self.host), str(self.port)))

        while True and not self.stop_request.isSet():
            try:
                r_topic, r_sender, r_data = request.recv_multipart()
                print " Received a request from " + r_sender + " to " + r_topic

                # de-serialize r_data
                ds_data = xMsgRegistrationData_pb2.xMsgRegistrationData()
                ds_data.ParseFromString(r_data)

                s_host = str(xMsgConstants.UNDEFINED)
                key = str(xMsgConstants.UNDEFINED)

                # Define the xMsg key
                if r_topic == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                    s_host = ds_data.domain
                else:
                    key = self._get_key(ds_data)

                if r_topic == str(xMsgConstants.REGISTER_PUBLISHER):
                    self.publishers_db[key] = ds_data

                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REGISTER_SUBSCRIBER):

                    self.subscribers_db[key] = ds_data
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REMOVE_PUBLISHER):
                    del self.publishers_db[key]
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REMOVE_SUBSCRIBER):
                    del self.subscribers_db[key]
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                    # Remove publishers registration data from a specified host
                    self._cleanDbByHost(s_host, self.publishers_db)

                    # Remove subscribers registration data from a specified host
                    self._cleanDbByHost(s_host, self.subscribers_db)
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.FIND_PUBLISHER):

                    res = self._getRegistration(ds_data.domain,
                                                ds_data.subject,
                                                ds_data.xtype,
                                                True)
                    request.send_multipart(self._reply_message(r_topic, res))

                elif r_topic == str(xMsgConstants.FIND_SUBSCRIBER):

                    res = self._getRegistration(ds_data.domain,
                                                ds_data.subject,
                                                ds_data.xtype,
                                                False)
                    request.send_multipart(self._reply_message(r_topic, res))
                else:
                    print " Warning: unknown registration request type..."

            except zmq.error.ContextTerminated:
                print " Context terminated at xMsgRegistrar"
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

        result = list()

        if isPublisher:
            for k in self.publishers_db:
                if ((xMsgUtil.get_domain(k) == domain) and
                        (xMsgUtil.get_subject(k) == subject or
                         subject == str(xMsgConstants.UNDEFINED) or
                         subject == str(xMsgConstants.ANY)) and
                        (xMsgUtil.get_type(k) == tip or
                         tip == str(xMsgConstants.UNDEFINED) or
                         tip == str(xMsgConstants.ANY))):
                    x = self.publishers_db[k]
                    result.append(x)
        else:
            for k in self.subscribers_db:
                if ((xMsgUtil.get_domain(k) == domain) and
                        (xMsgUtil.get_subject(k) == subject or
                         subject == str(xMsgConstants.UNDEFINED) or
                         subject == str(xMsgConstants.ANY)) and
                        (xMsgUtil.get_type(k) == tip or
                         tip == str(xMsgConstants.UNDEFINED) or
                         tip == str(xMsgConstants.ANY))):
                    x = self.subscribers_db[k]
                    result.append(x)
        return result

    def _get_key(self, ds_data):
        # Define the xMsg key
        key = ds_data.domain
        if ds_data.subject != str(xMsgConstants.UNDEFINED):
            key = key + ":" + ds_data.subject
        if ds_data.xtype != str(xMsgConstants.UNDEFINED):
            key = key + ":" + ds_data.xtype
        return key

    def _reply_success(self, topic):
        return [topic,
                xMsgUtil.get_local_ip() + ":" +
                str(xMsgConstants.REGISTRAR),
                str(xMsgConstants.SUCCESS)]

    def _reply_message(self, topic, res):
        d = [topic, xMsgUtil.get_local_ip() + ":" +
             str(xMsgConstants.REGISTRAR)]
        for rd in res:
            # Serialize and add to the reply message
            s_rd = rd.SerializeToString()
            d.append(s_rd)
        return d

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
        # Remove all identified keys
        for k in rk:
            db.remove(k)
