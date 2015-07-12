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
import re

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgExceptions import UndefinedTopicDomain, MalformedCanonicalName


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

    @classmethod
    def build(cls, domain, subject=ANY, xtype=ANY):
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
                    return cls(topic + SEPARATOR + t_arr)
            return cls(topic)

    @classmethod
    def wrap(cls, topic):
        return cls(topic)

    def domain(self):
        """
        Parses xMsg topic and returns domain of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: domain of the topic
        """
        try:
            return self._get_topic_group(self.topic, TOPIC_DOMAIN_GROUP)

        except:
            raise MalformedCanonicalName("xMsgTopic: undefined or malformed topic")


    def is_parent(self, other):
        return self.topic.startswith(str(other))

    def subject(self):
        """
        Parses xMsg topic and returns subject of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: subject of the topic
        """
        try:
            return self._get_topic_group(self.topic, TOPIC_SUBJECT_GROUP)

        except:
            raise MalformedCanonicalName("xMsgTopic: Received %s" %self.topic)

    def type(self):
        """
        Parses xMsg topic and returns type of the topic

        :param topic: xMsg topic constructed as domain:subject:xtype
        :return: type of the topic
        """
        try:
            return self._get_topic_group(self.topic, TOPIC_XTYPE_GROUP)

        except:
            raise MalformedCanonicalName("xMsgTopic: Received %s" %self.topic)

    def _get_topic_group(self, topic, group):
        match = TOPIC_VALIDATOR.match(topic)
        if match.group(group):
            return match.group(group)
        else:
            raise MalformedCanonicalName("xMsgTopic: Received %s" %self.topic)

    def __str__(self):
        return self.topic

