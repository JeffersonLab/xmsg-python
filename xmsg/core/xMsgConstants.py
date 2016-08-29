# coding=utf-8

from enum import Enum


class xMsgConstants(Enum):
    """xMsg Constants, helper class to define the constants used by the
    framework
    
    
    * UNDEFINED = (0, "undefined")
    * SUCCESS = (1, "success")
    * ANY = (2, "*")
    * REGISTRAR = (3, "xMsg_Registrar")
    * REGISTER_PUBLISHER = (4, "registerPublisher")
    * REGISTER_SUBSCRIBER = (5, "registerSubscriber")
    * REGISTER_REQUEST_TIMEOUT = (3000, "registerRequestTimeout")
    * REMOVE_PUBLISHER = (6, "removePublisherRegistration")
    * REMOVE_SUBSCRIBER = (7, "removeSubscriberRegistration")
    * REMOVE_ALL_REGISTRATION = (8, "removeAllRegistration")
    * REMOVE_REQUEST_TIMEOUT = (3000, "removeRequestTimeout")
    * FIND_REQUEST_TIMEOUT = (3000, "findRequestTimeout")
    * FIND_PUBLISHER = (9, "findPublisher")
    * FIND_SUBSCRIBER = (10, "findSubscriber")
    
    * INFO = (11, "info")
    * WARNING = (12, "warning")
    * ERROR = (13, "error")
    * NO_RESULT = (14, "none")
    * DONE = (15, "done")
    * DATA = (16, "data")
    * BIND = (17, "bind")
    * CONNECT = (18, "connect")
    
    * DEFAULT_PORT = (7771, "defaultPort")
    * REGISTRAR_PORT = (8888, "registrarPort")
    
    *Example 1*
    ::
        str(xMsgConstants.UNDEFINED)
        
        Gives: 'undefined'
        
    *Example 2*
    ::
        int(xMsgConstants.UNDEFINED)
        
        Gives: 0
    
    """
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

    CTRL_TOPIC = (19, "xmsg:control")
    CTRL_CONNECT = (20, "pub")
    CTRL_SUBSCRIBE = (21, "sub")
    CTRL_REPLY = (22, "rep")

    DEFAULT_PORT = (7791, "defaultPort")
    REGISTRAR_PORT = (8888, "registrarPort")

    def __init__(self, int_value, label):
        self.int_value = int_value
        self.label = label

    def __int__(self):
        return int(self.int_value)

    def __str__(self):
        return str(self.label)

    def get_string_value(self):
        """ Additional get string method. to keep consistance with xMsg Java

        Returns:
            String: string value of constant
        """
        return self.__str__()

    def get_int_value(self):
        """ Additional get int method. to keep consistance with xMsg Java

        Returns:
            int: integer value of constant
        """
        return self.__int__()
