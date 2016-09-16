# coding=ut-8

from xmsg.core.xMsgConstants import xMsgConstants


class xMsgRegResponse:
    """A wrapper for a response to a registration or discovery request.

    A response of the xMsgRegService registration service can be an string
    indicating that the request was successful, a set of registration data
    in case a discovery request was received, or an error description
    indicating that something wrong happened with the request.

    Attributes:
        topic (String): topic of the response message
        sender (String): response sender
        status (String): status of the request to respond
        data (bytes[]): registration data
    """

    def __init__(self, topic, sender, data=None, status=xMsgConstants.SUCCESS):
        self.topic = topic
        self.sender = sender
        self.status = status
        self.data = []

        if data is not None:
            for d in data:
                self.data.append(d)

    @classmethod
    def create_from_multipart_request(cls, request):
        """Returns (creates) a response object from multipart request

        Args:
            request (bytes[]): 0MQ multipart request

        Returns:
            xMsgRegResponse: response object
        """
        topic = request[0]
        sender = request[1]
        status = request[2]

        try:
            data = request[3]

        except IndexError:
            data = []

        finally:
            return cls(topic, sender, data, status)

    def get_topic(self):
        """Returns topic in the response

        Returns:
            String: response topic
        """
        return str(self.topic)

    def set_topic(self, topic):
        """Sets the topic in the response

        Args:
            topic (xMsgTopic): topic for the response
        """
        self.topic = topic

    def get_sender(self):
        """Returns the sender in the response

        Returns:
            String: response sender
        """
        return str(self.sender)

    def set_sender(self, sender):
        """Sets the sender in the response

        Args:
            sender (string): name of sender
        """
        self.sender = sender

    def get_status(self):
        """Returns request response status

        It can be xMsgConstants#SUCCESS or an error string indicating
        a problem with the request.

        Returns:
            String: status obtained from registration service
        """
        return str(self.status)

    def set_status(self, status):
        """Sets the status in the response

        Args:
            status (string): status by default is *success* otherwise
                an string indicating the error in the request
        """
        self.status = status

    def get_data(self):
        """Returns response data array

        Returns:
            bytes[]: data array from response
        """
        if len(self.data) is 0:
            return ""
        else:
            return self.data

    def msg(self):
        """Returns the response instance serialized

        Returns:
            bytes[]: serialized message for 0MQ
        """
        s_msg = [self.get_topic(), self.get_sender(), self.get_status()]

        for d in self.data:
            s_msg.append(str(d))
        return s_msg
