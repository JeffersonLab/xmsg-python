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

from xsys.regdis.xMsgRegDatabase import xMsgRegDatabase
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from data import xMsgRegistration_pb2


class xMsgRegistrationService(threading.Thread):
    '''
    The main registrar service, that always runs in a
    separate thread. Contains two separate databases
    to store publishers and subscribers registration data.
    The key for the data base is xMsg topic, constructed as:
    <b>domain:subject:type</b>
    Creates REP socket server on a default port
    Following request will be serviced:
    <ul>
        <li>Register publisher</li>
        <li>Register subscriber</li>
        <li>Find publisher</li>
        <li>Find subscriber</li>
    </ul>
    '''
    context = str(xMsgConstants.UNDEFINED)
    host = str(xMsgConstants.ANY)
    port = int(xMsgConstants.REGISTRAR_PORT)
    localhost_ip = str(xMsgConstants.UNDEFINED)
    subscribers_db = xMsgRegDatabase()
    publishers_db = xMsgRegDatabase()

    def __init__(self, context):
        super(xMsgRegistrationService, self).__init__()
        self.context = context
        self.localhost_ip = xMsgUtil.get_local_ip()
        self.stop_request = threading.Event()

    def run(self):
        request = self.context.socket(zmq.REP)
        request.bind("tcp://%s:%s" % (str(self.host), str(self.port)))

        while True and not self.stop_request.isSet():
            try:
                r_topic, r_sender, r_data = request.recv_multipart()
                print xMsgUtil.current_time() + " Received a request from " +\
                    r_sender + " to " + r_topic

                # de-serialize r_data
                ds_data = xMsgRegistration_pb2.xMsgRegistration()
                ds_data.ParseFromString(r_data)

                s_host = str(xMsgConstants.UNDEFINED)

                # Define the xMsg key
                if r_topic == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                    s_host = ds_data.domain

                if r_topic == str(xMsgConstants.REGISTER_PUBLISHER):
                    self.publishers_db.register(ds_data)
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REGISTER_SUBSCRIBER):
                    self.subscribers_db.register(ds_data)
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REMOVE_PUBLISHER):
                    self.publishers_db.remove(ds_data)
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REMOVE_SUBSCRIBER):
                    self.subscribers_db.remove(ds_data)
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                    # Remove publishers registration data from specified host
                    self._cleanDbByHost(s_host, self.publishers_db)
                    # Remove subscribers registration data from specified host
                    self._cleanDbByHost(s_host, self.subscribers_db)
                    # send a reply message
                    request.send_multipart(self._reply_success(r_topic))

                elif r_topic == str(xMsgConstants.FIND_PUBLISHER):
                    res = self.publishers_db.find(ds_data.domain,
                                                  ds_data.subject,
                                                  ds_data.type)
                    request.send_multipart(self._reply_message(r_topic, res))

                elif r_topic == str(xMsgConstants.FIND_SUBSCRIBER):

                    res = self.subscribers_db.find(ds_data.domain,
                                                   ds_data.subject,
                                                   ds_data.type)

                    request.send_multipart(self._reply_message(r_topic, res))
                else:
                    print " Warning: unknown registration request type..."

            except zmq.error.ContextTerminated:
                print " Context terminated at xMsgRegistrationService"
                return

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
        db = dict()
        for key in db.iterkeys():
            for registration in db.get(key):
                if registration.get_host() == host:
                    rk.append(registration)
            db.get(key).remove_all_children(rk)
            rk = []

    def _reply_success(self, topic):
        return [topic,
                xMsgUtil.get_local_ip() + ":" +
                str(xMsgConstants.REGISTRAR),
                str(xMsgConstants.SUCCESS)]

    def _reply_message(self, topic, res):
        d = [topic, xMsgUtil.get_local_ip() + ":" +
             str(xMsgConstants.REGISTRAR)]
        # Serialize and add to the reply message
        if len(res) != 0:
            res = [rd for rd in res]
        return d + res
