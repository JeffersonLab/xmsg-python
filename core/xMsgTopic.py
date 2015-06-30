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
from core.xMsgConstants import xMsgConstants
from core.xMsgExceptions import UndefinedTopicDomain, MalformedCanonicalName
import re

ANY = str(xMsgConstants.ANY)
SEPARATOR = ":"
TOPIC_PATTERN = "^([^: ]+)(:(\\w+)(:(\\w+))?)?$"
TOPIC_VALIDATOR = re.compile(TOPIC_PATTERN)
# Topic groups generated in the regular expression TOPIC_PATTERN
TOPIC_DOMAIN_GROUP = 1
TOPIC_SUBJECT_GROUP = 3
TOPIC_XTYPE_GROUP = 5


class xMsgTopic:
    
    topic = str(xMsgConstants.UNDEFINED)
    
    def __init__(self, topic):
        self.topic = topic

    @staticmethod
    def build(domain, subject=ANY, xtype=ANY):
        if (not domain or domain == str(xMsgConstants.UNDEFINED) or
                domain == ANY):
            raise UndefinedTopicDomain
        else:
            topic = domain
            if subject and subject != ANY:
                topic += SEPARATOR + subject
                if xtype and xtype != ANY:
                    t_arr = SEPARATOR.join([t for t in xtype.split(SEPARATOR)
                                            if t != ANY])
                    return xMsgTopic(topic + SEPARATOR + t_arr)
            return xMsgTopic(topic)

    @staticmethod
    def _get_topic_group(topic, group):
        match = TOPIC_VALIDATOR.match(topic)
        if match and match.group(group):
            return match.group(group)
        else:
            raise MalformedCanonicalName

    @staticmethod
    def wrap(topic):
        return xMsgTopic(topic)

    def domain(self):
        """
        Parses xMsg topic and returns domain of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: domain of the topic
        """
        try:
            domain = self._get_topic_group(self.topic, TOPIC_DOMAIN_GROUP)
        except MalformedCanonicalName:
            raise
        else:
            return domain

    def subject(self):
        """
        Parses xMsg topic and returns subject of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: subject of the topic
        """
        try:
            subject = self._get_topic_group(self.topic, TOPIC_SUBJECT_GROUP)
        except MalformedCanonicalName:
            raise
        else:
            return subject

    def type(self):
        """
        Parses xMsg topic and returns type of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: type of the topic
        """
        try:
            xtype = self._get_topic_group(self.topic, TOPIC_XTYPE_GROUP)
        except MalformedCanonicalName:
            raise
        else:
            return xtype
        
    def is_parent(self, other):
        return self.topic.startswith(str(other))

    def __str__(self):
        return self.topic

