#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

import netifaces as ni
import socket
import time
import re
from datetime import datetime

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.data import xMsgRegistration_pb2

__author__ = 'gurjyan'


class xMsgUtil:

    def __init__(self):
        pass

    @staticmethod
    def build_registration(name, description, domain, subject,
                           xtype, is_publisher):
        """xMsgRegistration builder util

        Args:
            name (String): registration name
            description (String): registration description
            domain (String): registration domain
            subject (String): registration subject
            xtype (String): registration type
            is_publisher (bool): True if registration is for a publisher
                actor otherwise means is a subscriber

        Returns:
            xMsgRegistration: xMsg registration object
        """
        r_data = xMsgRegistration_pb2.xMsgRegistration()
        r_data.name = name
        r_data.description = description
        r_data.host = xMsgUtil.get_local_ip()
        r_data.port = int(xMsgConstants.DEFAULT_PORT)
        r_data.domain = domain
        r_data.subject = subject
        r_data.type = xtype

        if is_publisher:
            r_data.ownerType = xMsgRegistration_pb2.xMsgRegistration.PUBLISHER
        else:
            r_data.ownerType = xMsgRegistration_pb2.xMsgRegistration.SUBSCRIBER

        return r_data

    @staticmethod
    def host_to_ip(hostname):
        """Converts host name to IP address representation

        Args:
            hostname (String): hostname to convert

        Returns
            String: IP address of the required host
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
        """Returns the local ip for xMsg actors

        Returns:
            String: local ip
        """
        try:
            # Gets the default gateway
            interface = str(ni.gateways()['default'][ni.AF_INET][1])
            return ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

        except Exception as e:
            raise("xMsgUtil.get_local_ip received : " + e)

    @staticmethod
    def is_ip(host_ip):
        """IP regex validator. Checks if the given hostname ip is a valid ip

        Args:
            host_ip (String): IP string to verify

        Returns:
            bool: true if its a valid IP number, otherwise False
        """
        c_pat = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}" + \
                           "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if c_pat.match(host_ip):
            return True
        else:
            return False

    @staticmethod
    def get_local_ips():
        """Returns list of local ips in the machine

        Returns:
            list: local ips in the machine
        """
        return ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])

    @staticmethod
    def list_to_string(list_to_convert):
        """List to string converter util

        Args:
            list_to_convert (list): list to convert into string

        Returns:
            String: converted string
        """
        return ', '.join(map(str, list_to_convert))

    @staticmethod
    def log(message):
        """Logger util, prints messages with timestamp in console

        Args:
            message (String): log message
        """
        print "%s %s" % (xMsgUtil.current_time(), str(message))

    @staticmethod
    def string_to_list(string_to_convert):
        """String to list converter util

        Args:
            string_to_convert (String): string to convert to list

        Returns:
            list: converted list
        """
        return string_to_convert.split(",")

    @staticmethod
    def sleep(seconds):
        """Sleep util, time is given in seconds

        Args:
            seconds (int): time to sleep in seconds
        """
        time.sleep(seconds)

    @staticmethod
    def keep_alive():
        """Keep alive method, keeps the execution alive indefinitely
        or until the program gets interrupted
        """
        while True:
            time.sleep(3)

    @staticmethod
    def current_time():
        """Returns the current time in format: %Y-%m-%d %H:%M:%S

        Returns:
            String: current time string 
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
