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
        self.connection = connection
        self.handle_thread = None

    def __repr__(self):
        return str("<xMsgSubscription : %s>" % self.topic)

    def is_alive(self):
        """ Checks if the thread is alive and running

        Returns:
            Bool: True if thread is running
        """
        return not self.handle_thread.stopped()

    def set_callback_func(self, callback):
        """ Sets handler function to execute in the background thread"""
        self.handle_thread = _Handler(self.topic, self.connection, callback)

    def start(self):
        """ Starts the subscription thread"""
        self.connection.subscribe(self.topic)
        if not self.connection.check_subscription(self.topic):
            self.connection.unsubscribe(self.topic)
        self.handle_thread.start()

    def stop(self):
        """ Stops the subscription thread"""
        self.handle_thread.stop()


class _Handler(Thread):
    """ Thread handler class"""

    def __init__(self, topic, connection, eval_func):
        """ Handler constructor

        Args:
            topic (str): topic for subscription
            connection (xMsgProxyDriver): driver for proxy connection
            eval_func (CallBack): callaback function
        """
        super(_Handler, self).__init__(name=topic)
        self.__connection = connection
        self.__connection.subscribe(topic)
        self.__is_running = Event()
        self.eval_func = eval_func

    def run(self):
        """ Starts the thread"""
        conn_poller = zmq.Poller()
        conn_poller.register(self.__connection.get_sub_socket(), zmq.POLLIN)

        while not self.stopped():
            try:
                socks = dict(conn_poller.poll(100))
                if socks.get(self.__connection.get_sub_socket()) == zmq.POLLIN:
                    t_data = self.__connection.recv()
                    if len(t_data) == 2:
                        continue
                    msg = xMsgMessage.create_with_serialized_data(t_data)
                    self.eval_func(msg)
            except zmq.error.ZMQError as e:
                self.stop()
                self.__connection.unsubscribe(self.name)
                raise e
        self.__connection.unsubscribe(self.name)

    def stop(self):
        """ Stops the thread"""
        self.__is_running.set()

    def stopped(self):
        """ Verify if thread as been stopped

        Returns:
            Bool: True if the thread has been ordered to stop
        """
        return self.__is_running.is_set()
