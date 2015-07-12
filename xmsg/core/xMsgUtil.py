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
from netifaces import AF_INET
import netifaces as ni
from datetime import datetime
import socket
import time

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.data import xMsgRegistration_pb2

__author__ = 'gurjyan'


class xMsgUtil:

    def __init__(self):
        pass

    @staticmethod
    def build_registration(name, description, domain, subject, xtype, is_publisher):
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
    def get_local_ip(n_iface='lo0'):
        try:
            return str(ni.ifaddresses(n_iface)[AF_INET][0]['addr'])
        except ValueError:
            xMsgUtil.log("xMsg received : " + str(n_iface))
            xMsgUtil.log("A valid network interface should be provided...")
            return

    @staticmethod
    def list_to_string(in_l):
        return ', '.join(map(str, in_l))

    @staticmethod
    def log(msg):
        print xMsgUtil.current_time() + " " + str(msg)

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
