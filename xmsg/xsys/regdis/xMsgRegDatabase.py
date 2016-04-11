# coding=utf-8

import re

from sets import Set
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.data import xMsgRegistration_pb2


class xMsgRegDatabase(object):
    """A registration database of xMsg actors.

    Actors are grouped by topic, i.e., actors registered with the same topic
    will be in the same group.

    Attributes:
        db (dict): dict() that stores the registration information
            for the xMsg actors.
    """

    def __init__(self):
        self.db = dict()

    def __str__(self):
        return str(self.db)

    def __repr__(self):
        return "<xMsgRegDatabase : %d items>" % len(self.db)

    def get(self, topic):
        """returns all data for specific topic
        Args:
            topic (String): topic of the register to retrieve

        Returns:
            bytes[]: serialized register data (serialized xMsgRegistration)
        """
        return self.db.get(str(topic))

    def register(self, registration_data):
        """Register the xMsg actor registration information

        Args:
            registration_data (xMsgRegistration): actor registration
                information
        """
        key = self._generate_key(registration_data)

        if registration_data is not None:
            if self.db.get(key):
                self.db[key].add(registration_data.SerializeToString())
            else:
                self.db[key] = Set()
                self.db[key].add(registration_data.SerializeToString())

    def remove(self, registration_data):
        """Removes specific registration from the database

        Args:
            registration_data (xMsgRegistration): actor registration
                information
        """
        key = self._generate_key(registration_data)
        r_data = registration_data.SerializeToString()
        if self.db.get(key):
            for db_data in self.db[key].copy():
                if db_data == r_data:
                    self.db[key].remove(db_data)
                    if len(self.db[key]) == 0:
                        del self.db[key]

    def remove_by_host(self, host):
        """Removes all stored registrations for specific hostname

        Method that removes all values of the registration database that
        have a specified host set, i.e.  removes registration information
        of all xMsg actors that are running on a specified host.

        Args:
            host (String): host name of the xMsg
        """
        for key in self.all():
            for r_data in self.db[key].copy():
                registration = xMsgRegistration_pb2.xMsgRegistration()
                registration.ParseFromString(r_data)
                if registration.host == host:
                    self.db.get(key).remove(r_data)
                    if len(self.db[key]) == 0:
                        del self.db[key]

    def find(self, domain, subject=str(xMsgConstants.ANY),
             xtype=str(xMsgConstants.ANY)):
        """Finds the registration information based on the topic composition

        The method will find registration from the following way

        - domain:*:* -> all registration for specific domain
        - domain:somesubject:* -> all registration for specific domain and subject
        - domain:somesubject:sometype -> all registration for specific topic

        Args:
            domain (string): registration domain
            subject (string): registration subject
            xtype (string): registration type

        Returns:
            Set: set of serialized registration data
        """
        if subject == "*" or subject == "undefined":
            subject = ":(.+)"
            xtype = ""

        else:
            subject = ":" + str(subject)
            if xtype == "*" or xtype == "undefined":
                xtype = ":(.)+"

            else:
                xtype = ":" + str(xtype)

        t_pattern = "^%s%s%s$" % (domain, subject, xtype)
        t_validator = re.compile(t_pattern)
        result = Set()

        for k in self.all():
            if t_validator.match(k):
                result.union_update(self.db[k])
                #result.intersection_update(self.db[k])

        if len(result) is 0:
            return None

        else:
            return result

    def all(self):
        """returns all topics

        Returns:
            list: list of all topics in the database
        """
        return self.db.keys()

    def clear(self):
        """clears the database, it will erase all data stored"""
        self.db.clear()
        self.db = dict()

    @staticmethod
    def _generate_key(registration_data):
        key = registration_data.domain
        if(registration_data.subject != str(xMsgConstants.UNDEFINED) and
           registration_data.subject != str(xMsgConstants.ANY)):
            key = key + ":" + registration_data.subject
        if(registration_data.type != str(xMsgConstants.UNDEFINED) and
           registration_data.type != str(xMsgConstants.ANY)):
            key = key + ":" + registration_data.type
        return key
