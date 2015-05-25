import threading

from core import xMsgUtil
from xsys.regdis.xMsgRegDiscDriver import xMsgRegDiscDriver


__author__ = 'gurjyan'


class xMsgFeRegT(xMsgRegDiscDriver, threading.Thread):
    """
    This is a thread that periodically updates xMsg front-end
    registration database with passed publishers and subscribers
    database contents. These passed databases (i.e. references)
    are xMsgNode resident databases, defined within the xMsgRegistrar class
    This class will be instantiated by the xMsgRegistrar constructor
    executed by the xMsgNode:

    This class inherits from {@link xMsgRegDiscDriver}
    where xMsg database communication methods are defined.

    """

    # xMsgNode database references
    publishers_db = dict()
    subscribers_db = dict()

    # Lock used to lock xMsgNode databases access
    lock = threading.Lock()

    def __init__(self, feHost, publisher_db, subscriber_db):
        xMsgRegDiscDriver.__init__(self, feHost)
        self.publishers_db = publisher_db
        self.subscribers_db = subscriber_db

    def run(self):
        while True:
            try:
                # update FE publishers database
                self.lock.acquire()
                try:
                    for key in self.publishers_db:
                        self.register_fe(key, self.publishers_db[key], True)
                        xMsgUtil.sleep(0.5)
                finally:
                    self.lock.release()

                # update FE subscribers database
                self.lock.acquire()
                try:
                    for key in self.subscribers_db:
                        self.register_fe(key, self.subscribers_db[key], False)
                        xMsgUtil.sleep(0.5)
                finally:
                    self.lock.release()

                for key in self.subscribers_db:
                    self.register_fe(key, self.subscribers_db[key], False)
                    xMsgUtil.sleep(0.5)

                xMsgUtil.sleep(5)
            except KeyboardInterrupt:
                return
