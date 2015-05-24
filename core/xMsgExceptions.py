'''
Created on 22-05-2015

@author: royarzun
'''


class MalformedCanonicalName(Exception):
    
    def __init__(self, message, topic):
        super(MalformedCanonicalName, self).__init__(message)
        self.message = message
        self.topic = "with topic: " + topic
        
    def __str__(self):
        return self.message + " " +self.topic
