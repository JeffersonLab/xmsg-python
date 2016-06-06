# coding=utf-8
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.xsys.regdis.xMsgRegDriver import xMsgRegDriver
from xmsg.xsys.pubsub.xMsgProxyDriver import xMsgProxyDriver


class ConnectionManager(object):

    def __init__(self, context):
        self.context = context
        self._proxy_connections = _ConnectionPool()
        self._reg_connections = _ConnectionPool()

    def create_registrar_connection(self, registration_address):
        """ Creates a new registrar connection from given registration address
        object

        Args:
            registration_address (RegAddress):

        Returns:
            xMsgRegDriver
        """
        return xMsgRegDriver(self.context, registration_address)

    def get_registrar_connection(self, registration_address):
        """ Returns registrar connection from given registration address object

        Args:
            registration_address (RegAddress): registrar address object

        Returns:
            xMsgRegDriver
        """
        cached_conn = self._reg_connections.get_connection(registration_address)
        if cached_conn:
            return cached_conn
        conn = xMsgRegDriver(self.context, registration_address)
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
            xMsgProxyDriver
        """
        conn = xMsgProxyDriver(proxy_address)
        conn.connect()
        if not conn.check_connection():
            raise Exception("Connection Manager: Could not connect...")
        return conn

    def get_proxy_connection(self, proxy_address):
        """ Returns proxy connection object from connection pool

        Args:
            proxy_address (ProxyAddress): proxy address object

        Returns:
            xMsgProxyDriver
        """
        cached_conn = self._proxy_connections.get_connection(proxy_address.host)
        if cached_conn:
            return cached_conn
        conn = xMsgProxyDriver(proxy_address)
        conn.connect()
        if not conn.check_connection():
            raise Exception("Connection Manager: Could not Connect...")
        return conn

    def release_proxy_connection(self, connection):
        """ Release proxy connection and caches it in the connection pool

        Args:
            connection (xMsgProxyDriver):
        """
        self._proxy_connections.set_connection(connection.get_address().host,
                                               connection)

    def destroy(self):
        # TODO: proper liberation of connection resources
        self.context.destroy()


class _ConnectionPool(object):

    def __init__(self):
        self._queue = {}

    def get_connection(self, address):
        try:
            return self._queue[address]
        except KeyError:
            return None

    def set_connection(self, address, connection):
        if not address in self._queue:
            self._queue[address] = connection

    def destroy_all(self):
        for connection in self._queue:
            connection.destroy()
