__author__ = 'gurjyan'

class xMsgConstants:

    def __init__(self):
        pass

    UNDEFINED = "undefined"
    SUCCESS = "success"
    ANY_HOST = "*"

    REGISTRAR = "xMsg_Registrar"

    REGISTER_PUBLISHER = "registerPublisher"
    REGISTER_SUBSCRIBER = "registerSubscriber"
    REGISTER_REQUEST_TIMEOUT = 3000

    REMOVE_PUBLISHER = "removePublisherRegistration"
    REMOVE_SUBSCRIBER = "removeSubscriberRegistration"
    REMOVE_ALL_REGISTRATION = "removeAllRegistration"
    REMOVE_REQUEST_TIMEOUT = 3000

    FIND_REQUEST_TIMEOUT = 3000
    FIND_PUBLISHER = "findPublisher"
    FIND_SUBSCRIBER = "findSubscriber"

    BIND = "bind"
    CONNECT = "connect"

    DEFAULT_PORT = 7771
    REGISTRAR_PORT = 8888

