import socket

__author__ = 'gurjyan'

class xMsgConstants:

    def __init__(self):
        pass

    UNDEFINED = b"undefined"
    SUCCESS = b"success"
    ANY = b"*"
    LOCALHOST = socket.gethostname()

    REGISTRAR = b"xMsg_Registrar"

    REGISTER_PUBLISHER = b"registerPublisher"
    REGISTER_SUBSCRIBER = b"registerSubscriber"
    REGISTER_REQUEST_TIMEOUT = 3000

    REMOVE_PUBLISHER = b"removePublisherRegistration"
    REMOVE_SUBSCRIBER = b"removeSubscriberRegistration"
    REMOVE_ALL_REGISTRATION = b"removeAllRegistration"
    REMOVE_REQUEST_TIMEOUT = 3000

    FIND_REQUEST_TIMEOUT = 3000
    FIND_PUBLISHER = b"findPublisher"
    FIND_SUBSCRIBER = b"findSubscriber"

    INFO = b"info"
    WARNING = b"warning"
    ERROR = b"error"

    NO_RESULT = b"none"
    DONE = b"done"

    BIND = b"bind"
    CONNECT = b"connect"

    DEFAULT_PORT = 7771
    REGISTRAR_PORT = 8888

