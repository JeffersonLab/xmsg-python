# coding=utf-8

from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver
from xmsg.xsys.pubsub.xMsgProxyDriver import xMsgProxyDriver


class ConnectionManager(object):

    def __init__(self, context):
        self.context = context
        self._proxy_connections = _ConnectionPool()
        self._reg_connections = _ConnectionPool()

    def create_registrar_connection(self, registration_address):
        """

        Args:
            registration_address (RegAddress):

        Returns:
            xMsgRegDriver
        """
        return xMsgRegDriver(self.context, registration_address)

    def get_registrar_connection(self, registration_address):
        """

        Args:
            registration_address:

        Returns:

        """
        cached_conn = self._reg_connections.get_connection(registration_address)
        if cached_conn:
            return cached_conn
        conn = xMsgProxyDriver(registration_address)
        conn.connect()
        return conn

    def release_registrar_connection(self, registrar_connection):
        """ Release registrar connection and lets it be cached for next usage

        Args:
            registrar_connection (xMsgRegDriver): connection to registrar
        """
        self._reg_connections.set_connection(registrar_connection.get_address(),
                                             registrar_connection)

    def create_proxy_connection(self, proxy_address):
        """ Creates a new proxy connection from given proxy_address object

        Args:
            proxy_address (ProxyAddress):

        Returns:

        """
        return xMsgProxyDriver(proxy_address)

    def get_proxy_connection(self, proxy_address):
        cached_conn = self._proxy_connections.get_connection(proxy_address)
        if cached_conn:
            return cached_conn
        conn = xMsgProxyDriver(proxy_address)
        conn.connect()
        return conn

    def release_proxy_connection(self, proxy_address):
        self._proxy_connections.set_connection(proxy_address.get_address(),
                                               proxy_address)

    def destroy(self):
        # TODO: proper liberation of connection resources
        self.context.destroy()


class _ConnectionPool(object):

    def __init__(self):
        self._queue = {}

    def get_connection(self, address):
        try:
            return self._queue[address.host]
        except KeyError:
            return None

    def set_connection(self, address, connection):
        if not self._queue.has_key(address):
            self._queue[address] = connection

    def destroy_all(self):
        for connection in self._queue:
            connection.destroy()
