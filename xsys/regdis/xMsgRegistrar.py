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
from data import xMsgRegistration_pb2
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

