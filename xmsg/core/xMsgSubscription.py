# coding=utf-8

import zmq

from threading import Thread, Event

from xmsg.core.xMsgMessage import xMsgMessage


class xMsgSubscription(object):
    """ A subscription object uses a xMsgConnection to receive xMsgMessage
    messages of the interested xMsgTopic topic, and calls a user action on
    every message.

    When the subscription is constructed, the connection will be subscribed to
    the topic, and a background thread will be started polling the connection
    for received messages. For every message, the user-provide callback will be
    executed.

    When the subscription is destroyed, the background thread will be stopped
    and the connection will be unsubscribed from the topic.

    Creation and destruction of subscriptions are controlled by the xMsg actor.
    """

    def __init__(self, topic, connection):
        """ xMsgSubscription constructor

        Args:
            topic (xMsgTopic): topic to subscribe xMsg actor
            connection (xMsgProxyDriver): driver to communicate with proxy
        """
        self.topic = str(topic)
        self._connection = connection
        self._handle_thread = None

    def __repr__(self):
        return str("<xMsgSubscription : %s>" % self.topic)

    def start(self, callback):
        """Starts the subscription thread

        Args:
            callback (xMsgCallback): callback function
        """
        self._handle_thread = self._Handler(self.topic, self._connection,
                                            callback)
        self._connection.subscribe(self.topic)
        if not self._connection.check_subscription(self.topic):
            self._connection.unsubscribe(self.topic)
        self._handle_thread.start()

    def stop(self):
        """Stops the subscription thread"""
        self._handle_thread.stop()

    class _Handler(Thread):
        """Thread handler class"""

        def __init__(self, topic, connection, handle):
            """ Handler constructor

            Args:
                topic (str): topic for subscription
                connection (xMsgProxyDriver): driver for proxy connection
                handle (func): callback function
            """
            super(xMsgSubscription._Handler, self).__init__(name=topic)
            self._connection = connection
            self._connection.subscribe(topic)
            self._is_running = Event()
            self.handle = handle

        def is_alive(self):
            return not self._is_running.isSet()

        def run(self):
            poller = zmq.Poller()
            poller.register(self._connection.get_sub_socket(), zmq.POLLIN)

            while not self._is_running.is_set():
                try:
                    socks = dict(poller.poll(100))
                    if socks.get(self._connection.get_sub_socket()) == zmq.POLLIN:
                        try:
                            t_data = self._connection.recv()
                            if len(t_data) == 2:
                                continue

                            msg = xMsgMessage.create_with_serialized_data(t_data)
                            self.handle(msg)
                        except Exception as e:
                            print e.message
                            continue
                except zmq.error.ZMQError as e:
                    if e.errno == zmq.ETERM:
                        break
                    print e.message

            self._connection.unsubscribe(self.name)

        def stop(self):
            self._is_running.set()
