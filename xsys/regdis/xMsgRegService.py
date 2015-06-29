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
from sets import Set
import threading
import zmq

from xsys.regdis.xMsgRegDatabase import xMsgRegDatabase
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from xsys.regdis.xMsgRegRequest import xMsgRegRequest
from xsys.regdis.xMsgRegResponse import xMsgRegResponse


class xMsgRegService(threading.Thread):
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

    subscribers_db = xMsgRegDatabase()
    publishers_db = xMsgRegDatabase()

    def __init__(self, context):
        super(xMsgRegService, self).__init__()
        self.context = context
        self.stop_request = threading.Event()

    def run(self):
        reg_socket = self.context.socket(zmq.REP)
        reg_socket.bind("tcp://%s:%s" % (str(self.host), str(self.port)))

        while True and threading.currentThread().is_alive():
            try:
                request = reg_socket.recv_multipart()
                if not request:
                    continue
                response = self.process_request(request)
                reg_socket.send_multipart(response.get_serialized_msg())
                del request
                del response

            except zmq.error.ContextTerminated:
                self.log("Context terminated at xMsgRegistrationService")
                return

    def process_request(self, recv_req):
        try:
            request = xMsgRegRequest()
            request.init_from_request(recv_req)
            registration = Set([])
            sender = xMsgUtil.get_local_ip() + ":" + str(xMsgConstants.REGISTRAR)
            
            msg = ("Received a request from " + request.get_sender() + " to " +
                   request.get_topic())
            self.log(msg)
            
            s_host = str(xMsgConstants.UNDEFINED)

            if request.get_topic() == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                s_host = request.get_data().domain

            if request.get_topic() == str(xMsgConstants.REGISTER_PUBLISHER):
                self.publishers_db.register(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REGISTER_SUBSCRIBER):
                self.subscribers_db.register(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REMOVE_PUBLISHER):
                self.publishers_db.remove(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REMOVE_SUBSCRIBER):
                self.subscribers_db.remove(request.get_data())

            elif request.get_topic() == str(xMsgConstants.REMOVE_ALL_REGISTRATION):
                self.subscribers_db.remove_by_host(s_host)
                self.publishers_db.remove_by_host(s_host)

            elif request.get_topic() == str(xMsgConstants.FIND_PUBLISHER):
                registration = self.publishers_db.find(request.get_data().domain,
                                                       request.get_data().subject,
                                                       request.get_data().type)
                self.log("RegService has found: " + str(len(registration)) +
                         " publishers" )

            elif request.get_topic() == str(xMsgConstants.FIND_SUBSCRIBER):
                registration = self.subscribers_db.find(request.get_data().domain,
                                                        request.get_data().subject,
                                                        request.get_data().type)
                self.log("RegService has found: " + str(len(registration)) +
                         " subscribers" )

            else:
                self.log("Warning: unknown registration request type...")
                self.log("Warning: received message : " + request.get_topic())
            # send a reply message
            return xMsgRegResponse(request.get_topic(), sender, registration)


        except zmq.error.ContextTerminated:
            self.log("Context terminated at xMsgRegistrationService")
            return

    def log(self, msg):
        # Logging behavior should be defined
        # Meaning storing messages or notifying to someone about the Event
        print xMsgUtil.current_time() + " " + msg
