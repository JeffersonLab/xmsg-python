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

from datetime import datetime
import socket
import fcntl
import struct
import time
import re

from core.xMsgExceptions import MalformedCanonicalName, UndefinedTopicDomain
from core.xMsgConstants import xMsgConstants

__author__ = 'gurjyan'

TOPIC_PATTERN = "^([^: ]+)(:(\\w+)(:(\\w+))?)?$"
TOPIC_VALIDATOR = re.compile(TOPIC_PATTERN)
TOPIC_SEP = ":"
# Topic groups generated in the regular expression TOPIC_PATTERN
TOPIC_DOMAIN_GROUP = 1
TOPIC_SUBJECT_GROUP = 3
TOPIC_XTYPE_GROUP = 5


class xMsgUtil:

    def __init__(self):
        pass

    @staticmethod
    def build_topic(domain, subject=None, xtype=None):
        if (not domain or domain == str(xMsgConstants.UNDEFINED) or
                domain == str(xMsgConstants.ANY)):
            raise UndefinedTopicDomain
        else:
            topic = domain
            if subject and subject != str(xMsgConstants.ANY):
                topic += TOPIC_SEP + subject
                if xtype and xtype != str(xMsgConstants.ANY):
                    t_arr = TOPIC_SEP.join([t for t in xtype.split(TOPIC_SEP)
                                            if t != str(xMsgConstants.ANY)])
                    return topic + TOPIC_SEP + t_arr
            return topic

    @staticmethod
    def _get_topic_group(topic, group):
        match = TOPIC_VALIDATOR.match(topic)
        if match and match.group(group):
            return match.group(group)
        else:
            raise MalformedCanonicalName

    @staticmethod
    def get_domain(topic):
        """
        Parses xMsg topic and returns domain of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: domain of the topic
        """
        try:
            domain = xMsgUtil._get_topic_group(topic, TOPIC_DOMAIN_GROUP)
        except MalformedCanonicalName:
            raise
        else:
            return domain

    @staticmethod
    def get_subject(topic):
        """
        Parses xMsg topic and returns subject of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: subject of the topic
        """
        try:
            subject = xMsgUtil._get_topic_group(topic, TOPIC_SUBJECT_GROUP)
        except MalformedCanonicalName:
            raise
        else:
            return subject

    @staticmethod
    def get_type(topic):
        """
        Parses xMsg topic and returns type of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: type of the topic
        """
        try:
            xtype = xMsgUtil._get_topic_group(topic, TOPIC_XTYPE_GROUP)
        except MalformedCanonicalName:
            raise
        else:
            return xtype

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

    @staticmethod
    def current_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
