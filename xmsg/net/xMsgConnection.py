# coding=utf-8

import zmq


class xMsgConnection(object):

    def __init__(self, connection_manager, proxy_driver):
        """

        Args:
            connection_manager (ConnectionManager):
            proxy_driver (xMsgProxyDriver):
        """
        self._pool = connection_manager
        self._connection = proxy_driver

    def get_address(self):
        return self._connection.get_address()

    def close(self):
        if self._connection:
            self._pool.release_proxy_connection(self._connection)
            self._connection = None

    def destroy(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def publish(self, msg):
        if not self._connection:
            raise Exception("Connection is closed")

        try:
            self._connection.send(msg)

        except zmq.ZMQError as e:
            self.destroy()
            raise e
