import socket
import fcntl
import struct
import time
import re

__author__ = 'gurjyan'

TOPIC_PATTERN = "^([^: ]+)(:(\\w+)(:(\\w+))?)?$"
TOPIC_VALIDATOR = re.compile(TOPIC_PATTERN)
TOPIC_SEP = ":"


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
        match = TOPIC_VALIDATOR.match(topic)
        if match:
            return match.group(1)
        else:
            raise Exception("ERROR: Malformed canonical name")

    @staticmethod
    def get_subject(topic):
        """
        Parses xMsg topic and returns subject of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: subject of the topic
        """
        match = TOPIC_VALIDATOR.match(topic)
        if match and match.group(3):
            return match.group(3)
        else:
            raise Exception("ERROR: Malformed canonical name")

    @staticmethod
    def get_type(topic):
        """
        Parses xMsg topic and returns type of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: type of the topic
        """
        match = TOPIC_VALIDATOR.match(topic)
        if match and match.group(5):
            return match.group(5)
        else:
            raise Exception("ERROR: Malformed canonical name")

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
        # Fix made by Aron to make xmsg-python get the right
        # local ip address.
        # We need to make some adjustment to get the right network
        # interface from the machine
        # TODO: Stablish how to define the current interface 
        ifname = "eth0"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

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
