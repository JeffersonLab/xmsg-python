# coding=utf-8

import zmq


class xMsgConnection(object):

    def __init__(self, address, pub_socket, sub_socket):
        self._address = address
        self._pub = pub_socket
        self._sub = sub_socket

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def sub_socket(self):
        return self._sub

    @sub_socket.setter
    def sub_socket(self, subscriber_socket):
        self._sub = subscriber_socket

    @property
    def pub_socket(self):
        return self._pub

    @pub_socket.setter
    def pub_socket(self, publisher_socket):
        self._pub = publisher_socket

    def send(self, message):
        self._pub.send(message.topic, zmq.SNDMORE)
        self._pub.send(message.metadata.SerializeToString(), zmq.SNDMORE)
        self._pub.send(message.data)

    def recv(self):
        return self._sub.recv_multipart()

    def subscribe(self, topic):
        self._sub.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe(self, topic):
        self._sub.setsockopt(zmq.UNSUBSCRIBE, topic)
