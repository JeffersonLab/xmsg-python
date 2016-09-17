# coding=utf-8

import multiprocessing as mp
import zmq

from threading import Thread, Event

from xmsg.core.xMsgSubscriptionExecutor import Executor
from xmsg.core.xMsgTopic import xMsgTopic


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

    def __init__(self, topic, connection, pool_size=1):
        """ xMsgSubscription constructor

        Args:
            topic (xMsgTopic): topic to subscribe xMsg actor
            connection (xMsgProxyDriver): driver to communicate with proxy
            pool_size (int): size of processing pool
        """
        self.topic = str(topic)
        self._connection = connection
        self._handle_thread = None
        self._pool_size = pool_size

    def __repr__(self):
        return str("<xMsgSubscription : %s>" % self.topic)

    def start(self, callback, publisher):
        """Starts the subscription thread

        Args:
            callback (xMsgCallback): callback function
            publisher (func): publisher function
        """
        self._handle_thread = self._Handler(self.topic,
                                            self._connection,
                                            callback,
                                            self._pool_size,
                                            publisher)

        self._connection.subscribe(self.topic)
        if not self._connection.check_subscription(self.topic):
            self._connection.unsubscribe(self.topic)
        self._handle_thread.start()

    def stop(self):
        """Stops the subscription thread"""
        self._handle_thread.stop()
        self._handle_thread.join()

    class _Handler(Thread):
        """Thread handler class"""

        def __init__(self, topic, driver, callback, pool_size, publisher):
            """ Handler constructor

            Args:
                topic (str): topic for subscription
                driver (xMsgProxyDriver): driver for proxy connection
                callback (func): callback function
                pool_size (int): processing pool size
                publisher (func): publisher function
            """
            super(xMsgSubscription._Handler, self).__init__(name=topic)
            self._callback = callback
            self._driver = driver
            self._driver.subscribe(topic)
            self._is_running = Event()
            self._pool_size = pool_size
            self._publisher = publisher

        def is_alive(self):
            return not self._is_running.isSet()

        def run(self):
            queue = mp.JoinableQueue()
            interruption_queue = mp.Queue()

            executor = Executor(queue, interruption_queue, self._callback)
            pool = mp.Pool(processes=self._pool_size, initializer=executor.run)

            poller = zmq.Poller()
            poller.register(self._driver.get_sub_socket(), zmq.POLLIN)
            while interruption_queue.empty() and not self._is_running.is_set():
                try:
                    socks = dict(poller.poll(100))
                    if socks.get(self._driver.get_sub_socket()) == zmq.POLLIN:
                        # serialized data received in the subscription
                        t_data = self._driver.recv()
                        if len(t_data) == 2:
                            continue
                        queue.put(t_data)

                except KeyboardInterrupt:
                    break

                except zmq.error.ZMQError as e:
                    if e.errno == zmq.ETERM:
                        self.stop()

            self._driver.unsubscribe(self.name)
            del queue
            del interruption_queue
            pool.close()
            pool.join()
            return

        def stop(self):
            self._is_running.set()
