# coding=utf-8


class xMsgConstants(object):
    """xMsgConstants, helper class defines the constants used by the framework
    """
    UNDEFINED = "undefined"
    SUCCESS = "success"
    ANY = "*"

    REGISTRAR = "xMsg_Registrar"

    REGISTER_PUBLISHER = "registerPublisher"
    REGISTER_SUBSCRIBER = "registerSubscriber"
    REGISTER_REQUEST_TIMEOUT = "registerRequestTimeout"

    REMOVE_PUBLISHER = "removePublisherRegistration"
    REMOVE_SUBSCRIBER = "removeSubscriberRegistration"
    REMOVE_ALL_REGISTRATION = "removeAllRegistration"
    REMOVE_REQUEST_TIMEOUT = "removeRequestTimeout"

    FIND_REQUEST_TIMEOUT = "findRequestTimeout"
    FIND_PUBLISHER = "findPublisher"
    FIND_SUBSCRIBER = "findSubscriber"

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

    NO_RESULT = "none"
    DONE = "done"
    DATA = "data"

    BIND = "bind"
    CONNECT = "connect"

    CTRL_TOPIC = "xmsg:control"
    CTRL_CONNECT = "pub"
    CTRL_SUBSCRIBE = "sub"
    CTRL_REPLY = "rep"

    DEFAULT_PORT = 7791
    DEFAULT_JAVA_PORT = 7771
    REGISTRAR_PORT = 8888
