'''
Created on 22-05-2015

@author: royarzun
'''


class RegistrationException(Exception):
    '''Exceptions related to registration issues'''
    pass


class MessageException(ValueError):
    '''Exceptions related to messaging'''
    pass


class TopicException(MessageException):
    '''Bad topic related exceptions'''
    pass


class MalformedCanonicalName(TopicException):
    '''Bad structure in the canonical name'''
    pass


class UndefinedTopicDomain(TopicException):
    pass


class TimeoutReached(RegistrationException):
    pass


class BadResponse(MessageException):
    pass
