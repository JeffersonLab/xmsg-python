# coding=utf-8

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


class xMsgTopic(object):
    """The main identification for xMsg pub/sub communications.

    xMsg is a *topic-based system*, and messages are published to given
    *topics*, or named channels, defined by *publishers*.
    *Subscribers* can received the messages published to the *topics*
    to which they are interested, by subscribing to them.

    In xMsg, a topic is composed of three parts: a *domain*, a
    *subject* and a *type*. Each part is separated by a semicolon
    character. The subject and the type can be omitted. Thus, the following
    topics are all valid:

    * *domain*
    * *domain:subject*
    * *domain:subject:type*

    The build factory method help to create a proper topic with the right
    format.

    When an xMsg actor is subscribed to a given topic, it will only receive
    messages published to that topic. To filter topics, the three  parts
    form a hierarchy, and all topics with the same prefix will be accepted.

    In other words, a subscriber listening for an specific *domain* will
    receive all messages whose topic starts with that domain, no matter the
    subject and the type. For example, if the subscription topic is "A",
    then all the messages with the following topics will be received:

    * *"A"*
    * *"A:B"*
    * *"A:C"*
    * *"A:B:1"*
    * *"A:C:1"*
    * *"A:C:2"*
    * etc...

    More specific subscriptions will not receive messages that match only the
    parent parts of the topic.
    Thus, subscription to *"A:B"* will accept *"A:B"*, *"A:B:1"*, *"A:B:2"*,
    etc, but will reject *"A"* or *"A:C"*
    Similarly, a subscription to *"A:B:1"* will only accept that exact topic,
    rejecting *"A:B:2"*, *"A:C"*, *"A"*, etc.
    """

    def __init__(self, topic):
        """xMsgTopic Constructor

        The topic string must be a valid xmsg topic
        """
        self.topic = topic

    def __repr__(self):
        return "<xMsgTopic: %s>" % self.topic

    def __str__(self):
        return self.topic

    @classmethod
    def build(cls, domain, subject=ANY, xtype=ANY):
        """xMsgTopic: xMsg valid topic builder

        Args:
            domain (string): topic domain
            subject (string): topic subject (default: ANY)
            type (string): topic type (default: ANY)

        Returns:
            xMsgTopic: valid xmsg topic object
        """
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
        """Use the given string as an xMsg topic. No validation is done to the string.

        The caller must be sure it is a valid topic.This factory method is
        provided for speed purposes. It should be used with caution.

        Args:
            topic (string): message topic

        Returns:
            xMsgTopic: xmsg topic object
        """
        return cls(topic)

    def domain(self):
        """Parses xMsg topic and returns domain of the topic

        Returns:
            Domain (String): domain of topic

        Raises:
            MalformedCanonicalName: if the topic is not properly formed
        """
        try:
            return self._get_topic_group(self.topic, TOPIC_DOMAIN_GROUP)

        except:
            raise MalformedCanonicalName("xMsgTopic: undefined or malformed topic")

    def is_parent(self, other):
        """Returns true if this topic is a parent of the given topic.

        A parent topic is a prefix of other topic, or they are the same.
        Examples:

        * "A" is a parent of "A:B" and "A:C:1"
        * "A" is NOT parent of "W:B" nor "Z"
        * "A:C" is a parent of "A:C:1" and "A:C"
        * "A:C" is NOT a parent of "A:B"

        A subscription to a parent topic will accept any children topic.
        See the class documentation for more details about filtering messages
        by topic.

        Args:
            other (xMsgTopic): the topic to match as a children

        Returns:
            boolean: True if this topic is a parent of the other
        """
        return str(other).startswith(str(self))

    def subject(self):
        """Parses xMsg topic and returns subject of the topic

        Returns:
            Subject (String): subject of the topic

        Raises:
            MalformedCanonicalName: if the topic is not properly formed
        """
        try:
            return self._get_topic_group(self.topic, TOPIC_SUBJECT_GROUP)

        except:
            raise MalformedCanonicalName("xMsgTopic: Received %s" % self.topic)

    def type(self):
        """Parses xMsg topic and returns type of the topic

        Returns:
            Type (String): type of the topic

        Raises:
            MalformedCanonicalName: if the topic is not properly formed
        """
        try:
            return self._get_topic_group(self.topic, TOPIC_XTYPE_GROUP)

        except:
            raise MalformedCanonicalName("xMsgTopic: Received %s" % self.topic)

    def _get_topic_group(self, topic, group):
        match = TOPIC_VALIDATOR.match(topic)
        if match.group(group):
            return match.group(group)
        else:
            raise MalformedCanonicalName("xMsgTopic: Received %s" % self.topic)
