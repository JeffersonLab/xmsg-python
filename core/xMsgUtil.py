import socket
import time
from core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'

class xMsgUtil:

    def __init__(self):
        pass

    @staticmethod
    def get_domain(topic):
        """
        Parses xMsg topic and returns domain of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: domain of the topic
        """
        if ":" not in topic:
            raise Exception("error: malformed canonical name.")
        else:
            st = topic.split(":")
            domain = st[0]
            return str(domain)

    @staticmethod
    def get_subject(topic):
        """
        Parses xMsg topic and returns subject of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: subject of the topic
        """
        if ":" not in topic:
            raise Exception("error: malformed canonical name.")
        else:
            st = topic.split(":")
            if len(st) < 2:
                raise Exception("error: malformed canonical name.")
            else:
                subject = st[1]
                return str(subject)

    @staticmethod
    def get_type(topic):
        """
        Parses xMsg topic and returns type of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: type of the topic
        """
        if ":" not in topic:
            raise Exception("error: malformed canonical name.")
        else:
            st = topic.split(":")
            if len(st) < 3:
                raise Exception("error: malformed canonical name.")
            else:
                xtype = st[2]
                return str(xtype)

    @staticmethod
    def host_to_ip(hostname):

        """
        Converts host name to IP address representation

        :param hostname:
        :return: IP address of the required host
        """
        if hostname == xMsgConstants.LOCALHOST:
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

    @staticmethod
    def keep_alive():
        while True:
            time.sleep(3)
