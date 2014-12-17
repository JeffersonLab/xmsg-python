import socket
import time

__author__ = 'gurjyan'

class xMsgUtil:

    def __init__(self):
        pass

    @staticmethod
    def host_to_ip(hostname):

        """
        Converts host name to IP address representation

        :param hostname:
        :return: IP address of the required host
        """
        if hostname == "localhost":
            return xMsgUtil.get_local_ip()
        else:
            if any(c.isalpha() for c in hostname):
                return socket.gethostbyname(hostname)
            else:
                return hostname

    @staticmethod
    def get_local_ip():
        local_host = socket.gethostbyname(socket.gethostname())
        return local_host

    @staticmethod
    def list_to_string(in_l):
        return ', '.join(map(str, in_l))

    @staticmethod
    def string_to_list(in_d):
        return in_d.split(",")

    @staticmethod
    def sleep(second):
        time.sleep(second)

