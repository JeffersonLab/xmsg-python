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
from enum import Enum

__author__ = 'gurjyan'


class xMsgConstants(Enum):
    UNDEFINED = (0, "undefined")
    SUCCESS = (1, "success")
    ANY = (2, "*")

    REGISTRAR = (3, "xMsg_Registrar")

    REGISTER_PUBLISHER = (4, "registerPublisher")
    REGISTER_SUBSCRIBER = (5, "registerSubscriber")
    REGISTER_REQUEST_TIMEOUT = (3000, "registerRequestTimeout")

    REMOVE_PUBLISHER = (6, "removePublisherRegistration")
    REMOVE_SUBSCRIBER = (7, "removeSubscriberRegistration")
    REMOVE_ALL_REGISTRATION = (8, "removeAllRegistration")
    REMOVE_REQUEST_TIMEOUT = (3000, "removeRequestTimeout")

    FIND_REQUEST_TIMEOUT = (3000, "findRequestTimeout")
    FIND_PUBLISHER = (9, "findPublisher")
    FIND_SUBSCRIBER = (10, "findSubscriber")

    INFO = (11, "info")
    WARNING = (12, "warning")
    ERROR = (13, "error")

    NO_RESULT = (14, "none")
    DONE = (15, "done")
    DATA = (16, "data")

    BIND = (17, "bind")
    CONNECT = (18, "connect")

    DEFAULT_PORT = (7771, "defaultPort")
    REGISTRAR_PORT = (8888, "registrarPort")

    def __init__(self, int_value, label):
        self.int_value = int_value
        self.label = label

    def __int__(self):
        return int(self.int_value)

    def __str__(self):
        return str(self.label)

    def get_string_value(self):
        return self.__str__()

    def get_int_value(self):
        return self.__int__()
